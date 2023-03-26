import tkinter as tk
from tkinter import ttk
from collections import deque


class PomodoroTimer(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Pomodoro Timer")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        container = ttk.Frame(self)
        container.grid()
        container.columnconfigure(0, weight=1)

        timer_frame = Timer(container)
        timer_frame.grid(row=0, column=0, sticky="NESW")


class Timer(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.timer_order = ["Pomodoro", "Short Break", "Pomodoro", "Short Break", "Pomodoro", "Long Break"]
        self.timer_schedule = deque(self.timer_order)

        self.current_time = tk.StringVar(value="00:10")
        self.timer_running = True

        timer_frame = ttk.Frame(self, height="100")
        timer_frame.grid(row=0, column=0, pady=(10, 0), sticky="NESW")

        timer_counter = ttk.Label(timer_frame, textvariable=self.current_time)
        timer_counter.grid(row=0, column=0)

        self.decrement_timer()

    def decrement_timer(self):
        current_time = self.current_time.get()
        if self.timer_running and current_time != "00:00":
            minutes, seconds = current_time.split(":")

            if int(seconds) > 0:
                seconds = int(seconds) - 1
                minutes = int(minutes)
            else:
                seconds = 59
                minutes = int(minutes) - 1

            self.current_time.set(f"{minutes:02d}:{seconds:02d}")
            self.after(1000, self.decrement_timer)  # run decrement after 1 second
        elif self.timer_running and current_time == "00:00":
            self.timer_schedule.rotate(-1)
            next_up = self.timer_schedule[0]

            if next_up == "Pomodor":
                self.current_time.set("25:00")
            elif next_up == "Short Break":
                self.current_time.set("05:00")
            elif next_up == "Long Break":
                self.current_time.set("15:00")
            # go fo next round in the deque
            self.after(1000, self.decrement_timer)


if __name__ == "__main__":
    app = PomodoroTimer()
    app.mainloop()
