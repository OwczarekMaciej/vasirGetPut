import tkinter as tk
from tkinter import ttk
import threading
import time

class AudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Recording App")
        self.is_recording = False
        self.is_waiting = False
        
        # Label to show the status
        self.status_label = tk.Label(root, text="Ready to record", font=("Arial", 14))
        self.status_label.pack(pady=20)

        # Start Recording Button
        self.start_button = ttk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=10)

        # Stop Recording Button (initially disabled)
        self.stop_button = ttk.Button(root, text="Stop Recording", command=self.stop_recording, state="disabled")
        self.stop_button.pack(pady=10)

        # Visual effect (color change)
        self.visual_label = tk.Label(root, text="", width=30, height=2, bg="lightgray")
        self.visual_label.pack(pady=20)

    def start_recording(self):
        # Update status and button states
        self.is_recording = True
        self.status_label.config(text="Recording...")
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

        # Start the visual effect
        self.start_visual_effect()

        # Start the recording in a separate thread to avoid blocking the GUI
        threading.Thread(target=self.record_audio).start()

    def stop_recording(self):
        # Update recording status
        self.is_recording = False
        self.status_label.config(text="Sending audio...")
        self.stop_visual_effect()

        # Change button states
        self.stop_button.config(state="disabled")

        # Send and wait for response in a separate thread
        threading.Thread(target=self.send_and_receive_audio).start()

    def record_audio(self):
        # Integrate your audio recording code here
        time.sleep(5)  # Simulate a recording delay for demo purposes

    def send_and_receive_audio(self):
        # Integrate your code to send and receive audio here

        # Simulate waiting for a response
        self.is_waiting = True
        self.start_waiting_effect()
        time.sleep(3)  # Simulate server response time
        self.is_waiting = False
        self.stop_waiting_effect()

        # Update status and reset button states
        self.status_label.config(text="Ready to record")
        self.start_button.config(state="normal")

    def start_visual_effect(self):
        def animate():
            colors = ["red", "orange", "yellow"]
            i = 0
            while self.is_recording:
                self.visual_label.config(bg=colors[i % len(colors)])
                i += 1
                time.sleep(0.3)
        threading.Thread(target=animate).start()

    def stop_visual_effect(self):
        self.visual_label.config(bg="lightgray")

    def start_waiting_effect(self):
        self.status_label.config(text="Waiting for response...", fg="blue")

    def stop_waiting_effect(self):
        self.status_label.config(fg="black")

# Run the application
root = tk.Tk()
app = AudioApp(root)
root.mainloop()
