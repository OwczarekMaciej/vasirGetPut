import tkinter as tk
import threading
import itertools
import recordAudio
import putAudio
import getAudio
import time
import os

class VasirApp:
    MAIN_BG = "#1E1E1E"          # Bardzo ciemne tło
    PRIMARY_COLOR = "#007BFF"    # Akcent / Kolor domyślny
    SUCCESS_COLOR = "#28A745"    # Start / Nagrywanie
    ERROR_COLOR = "#DC3545"      # Stop / Błąd
    TEXT_COLOR = "#FFFFFF"       # Biały tekst
    
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.initialize_variables()

        frame = tk.Frame(root, bg=self.MAIN_BG)
        frame.pack(expand=True, fill='both', padx=50, pady=50)

        frame.grid_columnconfigure(0, weight=1)

        self.setup_toggle_button(frame)
        self.setup_labels(frame)

    def setup_window(self):
        self.root.title("VASIR Voice Assistant")
        self.root.geometry("600x400")
        self.root.config(bg=self.MAIN_BG)
    
    def initialize_variables(self):
        self.stop_event = threading.Event()
        self.recording_thread = None
        self.loading_thread = None
        self.is_recording = False
        self.filename = "output.wav"
        self.api_url_upload = "https://apzna1a8ci.execute-api.eu-north-1.amazonaws.com/test/upload"
        self.api_url_download = "https://apzna1a8ci.execute-api.eu-north-1.amazonaws.com/test/"

    def setup_toggle_button(self, frame):
        self.toggle_button = tk.Button(frame, text="Start Recording", command=self.toggle_recording,
                                       font=("Segoe UI", 18, "bold"), 
                                       bg=self.SUCCESS_COLOR, fg="black",
                                       width=18, height=2, relief="flat", bd=0, 
                                       activebackground=self.SUCCESS_COLOR)
        
        self.configure_button(self.toggle_button, self.SUCCESS_COLOR)
        self.toggle_button.grid(row=0, column=0, pady=(0, 20), sticky="n")

    def configure_button(self, button, highlight_color):
        pass 

    def setup_labels(self, frame):
        self.title_label = tk.Label(frame, text="VASIR - Voice Assistant",
                                    font=("Segoe UI", 20, "bold"), 
                                    bg=self.MAIN_BG, fg=self.TEXT_COLOR)
        self.title_label.grid(row=0, column=0, pady=(20, 10), sticky="n")

        self.toggle_button.grid(row=1, column=0, pady=(20, 20), sticky="n")

        self.status_label = tk.Label(frame, text="Press Start to activate voice command", 
                                     font=("Segoe UI", 14), bg=self.MAIN_BG, fg=self.TEXT_COLOR)
        self.status_label.grid(row=2, column=0, pady=5)

        self.loading_label = tk.Label(frame, text="", font=("Segoe UI", 12), 
                                      bg=self.MAIN_BG, fg=self.TEXT_COLOR)
        self.loading_label.grid(row=3, column=0, pady=5)


    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.stop_event.clear()
        self.is_recording = True
        self.update_ui_start_recording()

        self.recording_thread = threading.Thread(target=self.record_audio)
        self.recording_thread.start()

    def stop_recording(self):
        self.stop_event.set()
        if self.recording_thread:
            self.recording_thread.join()

        self.is_recording = False
        self.status_label.config(text="Uploading audio...", fg=self.PRIMARY_COLOR)
        self.toggle_button.config(text="Start Recording", bg=self.SUCCESS_COLOR)

        threading.Thread(target=self.upload_and_get_response).start()

    def update_ui_start_recording(self):
        self.toggle_button.config(text="Stop Recording", bg=self.ERROR_COLOR)
        self.status_label.config(text="🔴 Recording... Say your command", fg=self.ERROR_COLOR)

    def record_audio(self):
        recordAudio.record_audio(self.stop_event)

    def upload_and_get_response(self):
        try:
            response_filename = putAudio.upload_audio_file(self.api_url_upload, self.filename)
            if response_filename:
                self.status_label.config(text="Uploaded. Waiting for response...", fg=self.PRIMARY_COLOR)
                self.start_loading_animation()
                self.poll_for_response_audio(response_filename)
            else:
                self.status_label.config(text="Upload failed. Check connection.", fg=self.ERROR_COLOR)
        except Exception as e:
            self.status_label.config(text=f"Error: {e}", fg=self.ERROR_COLOR)

    def poll_for_response_audio(self, response_filename):
        while True:
            try:
                audio_data = getAudio.get_audio_file(self.api_url_download, response_filename)
                if audio_data:
                    with open("response_audio.mp3", "wb") as f:
                        f.write(audio_data)

                    self.status_label.config(text="✅ Response received. Playing audio...", fg=self.SUCCESS_COLOR)
                    self.stop_loading_animation()
                    self.play_audio("response_audio.mp3")
                    break
                else:
                    self.status_label.config(text="⏳ Waiting for response...", fg=self.PRIMARY_COLOR)
            except Exception as e:
                self.status_label.config(text=f"Error during retrieval: {e}", fg=self.ERROR_COLOR)

            time.sleep(1)

    def play_audio(self, filename):
        os.system(f"afplay {filename}")
        self.status_label.config(text="Playback complete. Ready.", fg=self.TEXT_COLOR)

    def start_loading_animation(self):
        self.loading_label.config(text="Waiting...")
        self.loading_animation_active = True
        self.loading_thread = threading.Thread(target=self.animate_loading)
        self.loading_thread.start()

    def stop_loading_animation(self):
        self.loading_animation_active = False
        if self.loading_thread and self.loading_thread.is_alive():
            self.loading_thread.join() 
        self.loading_label.config(text="")

    def animate_loading(self):
        loading_text = "..."
        while self.loading_animation_active:
            for i in range(4):
                if not self.loading_animation_active:
                    break
                dots = loading_text[:i]
                self.loading_label.config(text=f"Processing{dots}")
                time.sleep(0.3)
            
            if not self.loading_animation_active:
                break


root = tk.Tk()
app = VasirApp(root)
root.mainloop()