import tkinter as tk
import threading
import itertools
import recordAudio
import putAudio
import getAudio
import time
import os

class VasirApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.initialize_variables()

        # Frame for content alignment
        frame = tk.Frame(root, bg=self.bg_color)
        frame.pack(expand=True)

        # Setup UI elements
        self.setup_toggle_button(frame)
        self.setup_labels(frame)

    def setup_window(self):
        """Configure the main window settings."""
        self.root.title("VASIR")
        self.root.geometry("600x400")
        self.bg_color = "#2E2E2E"
        self.root.config(bg=self.bg_color)
    
    def initialize_variables(self):
        """Initialize the application variables."""
        self.stop_event = threading.Event()
        self.recording_thread = None
        self.loading_thread = None
        self.is_recording = False
        self.filename = "output.wav"
        self.api_url_upload = "https://apzna1a8ci.execute-api.eu-north-1.amazonaws.com/dev/upload"
        self.api_url_download = "https://apzna1a8ci.execute-api.eu-north-1.amazonaws.com/dev"

    def setup_toggle_button(self, frame):
        """Create and configure the toggle button."""
        self.toggle_button = tk.Button(frame, text="Start Recording", command=self.toggle_recording,
                                       font=("Helvetica", 16, "bold"), bg="#4CAF50", fg="black",
                                       width=20, height=2, relief="solid", bd=1)
        self.configure_button(self.toggle_button, highlight_color="#4CAF50")
        self.toggle_button.grid(row=0, column=0, pady=(50, 10), padx=10)

    def configure_button(self, button, highlight_color):
        """Apply common configurations to a button."""
        button.config(highlightbackground=highlight_color, highlightcolor=highlight_color, borderwidth=2)
        button.bind("<Enter>", lambda event: button.config(highlightbackground="#FF5722"))
        button.bind("<Leave>", lambda event: button.config(highlightbackground=highlight_color))

    def setup_labels(self, frame):
        """Create and configure the status and loading labels."""
        self.status_label = tk.Label(frame, text="Press 'Start Recording' to begin", 
                                     font=("Helvetica", 14), bg=self.bg_color, fg="white")
        self.status_label.grid(row=1, column=0, pady=10)

        self.loading_label = tk.Label(frame, text="", font=("Helvetica", 12), 
                                      bg=self.bg_color, fg="white")
        self.loading_label.grid(row=2, column=0, pady=10)

    def toggle_recording(self):
        """Handle the toggle button click to start/stop recording."""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        """Begin recording audio."""
        self.stop_event.clear()
        self.is_recording = True
        self.update_ui_start_recording()

        self.recording_thread = threading.Thread(target=self.record_audio)
        self.recording_thread.start()

    def stop_recording(self):
        """Stop recording audio."""
        self.stop_event.set()
        self.recording_thread.join()

        self.is_recording = False
        self.status_label.config(text="Uploading audio...", fg="white")
        self.toggle_button.config(text="Start Recording", bg="#4CAF50")

        threading.Thread(target=self.upload_and_get_response).start()

    def update_ui_start_recording(self):
        """Update UI components to reflect recording status."""
        self.toggle_button.config(text="Stop Recording", bg="#FF5722")
        self.status_label.config(text="Recording...", fg="white")

    def record_audio(self):
        """Handle the audio recording."""
        recordAudio.record_audio(self.stop_event)

    def upload_and_get_response(self):
        """Upload the recorded audio and wait for a response."""
        try:
            response_filename = putAudio.upload_audio_file(self.api_url_upload, self.filename)
            if response_filename:
                self.status_label.config(text="Uploaded. Waiting for response...", fg="white")
                self.start_loading_animation()
                self.poll_for_response_audio(response_filename)
            else:
                self.status_label.config(text="Failed to upload audio.", fg="red")
        except Exception as e:
            self.status_label.config(text=f"Error: {e}", fg="red")

    def poll_for_response_audio(self, response_filename):
        """Poll the server for a response audio file."""
        while True:
            try:
                audio_data = getAudio.get_audio_file(self.api_url_download, response_filename)
                if audio_data:
                    with open("response_audio.mp3", "wb") as f:
                        f.write(audio_data)

                    self.status_label.config(text="Response received. Playing audio...", fg="white")
                    self.stop_loading_animation()
                    self.play_audio(response_filename)
                    break
                else:
                    self.status_label.config(text="Waiting for response...", fg="white")
            except Exception as e:
                self.status_label.config(text=f"Error during retrieval: {e}", fg="red")

            time.sleep(1)

    def play_audio(self, filename):
        """Play the received audio file."""
        os.system(f"afplay {filename}")
        self.status_label.config(text="Playback complete", fg="white")

    def start_loading_animation(self):
        """Start an animation to indicate loading status."""
        self.loading_label.config(text="Waiting...")
        self.loading_animation_active = True
        self.loading_thread = threading.Thread(target=self.animate_loading)
        self.loading_thread.start()

    def stop_loading_animation(self):
        """Stop the loading animation."""
        self.loading_animation_active = False
        self.loading_thread.join()
        self.loading_label.config(text="")

    def animate_loading(self):
        """Animate the loading label with rotating symbols."""
        loading_symbols = itertools.cycle(['|', '/', '-', '\\'])
        while self.loading_animation_active:
            symbol = next(loading_symbols)
            self.loading_label.config(text=f"Waiting {symbol}")
            time.sleep(0.2)

# Create the main application window
root = tk.Tk()
app = VasirApp(root)
root.mainloop()