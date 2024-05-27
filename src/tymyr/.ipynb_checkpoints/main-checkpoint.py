import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

class TimerWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("TYMYR")

        # Manually setting a neutral background color
        background_color = 'ivory2'  # You can change this to any specific color if needed

        # Configure the window's overall background color
        self.master.configure(bg=background_color)

        # Initialize the elapsed time and running state
        self.elapsed_time = timedelta(0)
        self.running = False
        self.last_time = datetime.now()

        # Create the timer display label with a consistent background
        self.timer_label = tk.Label(self.master, text="00:00:00", font=("Helvetica", 20), bg=background_color)
        self.timer_label.pack(padx=10, pady=10, ipadx=5, ipady=5)

        # Create a frame for the buttons with a consistent background color
        controls_frame = tk.Frame(self.master, bg=background_color)
        controls_frame.pack(padx=5, pady=5)

        # Start button with consistent background
        self.start_button = tk.Button(controls_frame, text="Start", command=self.start, font=("Helvetica", 12), bg=background_color, relief=tk.GROOVE)
        self.start_button.pack(side="left", padx=5)

        # Stop button with consistent background
        self.stop_button = tk.Button(controls_frame, text="Stop", command=self.stop, font=("Helvetica", 12), bg=background_color, relief=tk.GROOVE)
        self.stop_button.pack(side="left", padx=5)

        # Reset button with consistent background
        self.reset_button = tk.Button(controls_frame, text="Reset", command=self.reset, font=("Helvetica", 12), bg=background_color, relief=tk.GROOVE)
        self.reset_button.pack(side="left", padx=5)

        # Update the timer every 100ms
        self.update_timer()

    def start(self):
        if not self.running:
            self.running = True
            self.last_time = datetime.now()

    def stop(self):
        if self.running:
            self.running = False
            self.elapsed_time += datetime.now() - self.last_time

    def reset(self):
        self.stop()
        self.elapsed_time = timedelta(0)
        self.timer_label.config(text="00:00:00")

    def update_timer(self):
        if self.running:
            current_time = datetime.now()
            delta = current_time - self.last_time
            elapsed = self.elapsed_time + delta
            self.timer_label.config(text=str(elapsed).split('.')[0])
        self.master.after(100, self.update_timer)

def main():
    root = tk.Tk()
    app = TimerWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()