import tkinter as tk
from tkinter import messagebox
import time
import threading
import subprocess
import os

# Time Intervals in Seconds
THEORY_TIME = 15*60
PRACTICE_TIME = 15*60
BREAK_TIME = 15*60

# Sound path
bell_sound = os.path.join(os.path.dirname(__file__), "bell.wav")

class TimerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Timer Application")

        self.label = tk.Label(root, text="Ready", font=("Helvetica", 32))
        self.label.pack(pady=20)

        self.start_button = tk.Button(root, text="Start Learning Cycle", font=("Helvetica", 16), command=self.start_cycle)
        self.start_button.pack(pady=10)

        self.pause_button = tk.Button(root, text="Pause", font=("Helvetica", 16), command=self.pause_timer)
        self.pause_button.pack(pady=10)

        self.timer_thread = None
        self.running = False
        self.paused = False
        self.pause_event = threading.Event()
        self.pause_event.set()

    def start_cycle(self):
        if self.running:
            return
        self.running = True
        self.timer_thread = threading.Thread(target=self.run_cycle)
        self.timer_thread.start()

    def run_cycle(self):
        self.run_timer("Theory Time", THEORY_TIME)
        self.play_bell()

        self.run_timer("Practice Time", PRACTICE_TIME)
        self.play_bell()

        self.run_timer("Break Time Time", BREAK_TIME)
        self.play_bell()

        self.label.config(text="Cycle Complete")
        self.play_bell()
        
        self.running = False

    def run_timer(self, phase_name, duration):
        for remaining in range(duration, 0, -1):
            self.pause_event.wait()

            mins, secs = divmod(remaining, 60)
            self.label.config(text=f"{phase_name}:{mins:02}:{secs:02}")
            time.sleep(1)
        self.label.config(text=f"{phase_name} Done!")

    def pause_timer(self):
        if self.paused:
            self.paused = False
            self.pause_event.set()
            self.pause_button.config(text="Pause")
        else:
            self.paused = True
            self.pause_event.clear()
            self.pause_button.config(text="Resume")

    def play_bell(self):
        try:
            print("Sound file exists:", os.path.exists(bell_sound))
            subprocess.run(["ffplay", "-nodisp", "-autoexit", bell_sound], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            messagebox.showerror("Error", f"Couldn't play sound: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()