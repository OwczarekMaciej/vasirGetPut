import tkinter as tk
import threading
import recordAudio
import putAudio

class AudioRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Recorder")

        self.stop_event = threading.Event()
        self.recording_thread = None
        self.is_recording = False

        self.toggle_button = tk.Button(root, text="Start Recording", command=self.toggle_recording)
        self.toggle_button.pack(pady=10)

        self.status_label = tk.Label(root, text="Press 'Start Recording' to begin")
        self.status_label.pack(pady=10)

    def toggle_recording(self):
        if not self.is_recording:
            # Start recording
            self.start_recording()
        else:
            # Stop recording
            self.stop_recording()

    def start_recording(self):
        # Clear the stop event and create a new recording thread
        self.stop_event.clear()
        self.recording_thread = threading.Thread(target=self.record_audio)

        # Update button and status label
        self.toggle_button.config(text="Stop Recording")
        self.status_label.config(text="Recording...")
        self.is_recording = True

        # Start the recording thread
        self.recording_thread.start()

    def stop_recording(self):
        # Set the stop event to signal the recording thread to stop
        self.stop_event.set()

        # Wait for the recording thread to finish
        self.recording_thread.join()

        putAudio.upload_audio_file("output.wav")
        # Update button and status label
        self.toggle_button.config(text="Start Recording")
        self.status_label.config(text="Recording stopped and saved as output.wav")
        self.is_recording = False

    def record_audio(self):
        recordAudio.record_audio(self.stop_event)

root = tk.Tk()
app = AudioRecorderApp(root)
root.mainloop()
