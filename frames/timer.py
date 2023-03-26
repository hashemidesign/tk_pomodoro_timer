import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from collections import deque


class Timer(ttk.Frame):
    def __init__(self, parent, controller, show_settings):
        super().__init__(parent)
        self.controller = controller

        pomodoro_time = int(self.controller.pomodoro.get())
        self.current_time = tk.StringVar(value=f"{pomodoro_time:02d}:00")
        self.timer_running = False
        # Timer Description
        self.current_timer_label = tk.StringVar(value=self.controller.timer_schedule[0])
        timer_description = ttk.Label(self, textvariable=self.current_timer_label)
        timer_description.grid(row=0, column=0, sticky="W", padx=(10, 0), pady=(10, 0))
        # track current timer
        self._timer_decrement_job = None

        settings_button = ttk.Button(self, text="Settings", command=show_settings, cursor="hand2")
        settings_button.grid(row=0, column=1, sticky="E", padx=10, pady=(10, 0))

        timer_frame = ttk.Frame(self, height="100")
        timer_frame.grid(row=1, pady=(10, 0), sticky="NESW", columnspan=2)

        timer_counter = ttk.Label(timer_frame, textvariable=self.current_time)
        timer_counter.place(relx=0.5, rely=0.5, anchor="center")

        # Setting up start/stop buttons
        button_container = ttk.Frame(self, padding=10)
        button_container.grid(row=2, column=0, sticky="EW", columnspan=2)
        button_container.columnconfigure((0, 1, 2), weight=1)

        self.start_button = ttk.Button(button_container,
                                       text="Start",
                                       command=self.start_timer,
                                       cursor="hand2")
        self.stop_button = ttk.Button(button_container,
                                      text="Stop",
                                      command=self.stop_timer,
                                      cursor="hand2",
                                      state="disabled")
        self.reset_button = ttk.Button(button_container,
                                       text="Reset",
                                       command=self.reset_timer,
                                       cursor="hand2")
        self.start_button.grid(row=0, column=0, sticky="EW")
        self.stop_button.grid(row=0, column=1, sticky="EW", padx=5)
        self.reset_button.grid(row=0, column=2, sticky="EW")

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
            self._timer_decrement_job = self.after(1000, self.decrement_timer)  # run decrement after 1 second
        elif self.timer_running and current_time == "00:00":
            self.controller.timer_schedule.rotate(-1)
            next_up = self.controller.timer_schedule[0]
            self.current_timer_label.set(next_up)

            if next_up == "Pomodoro":
                pomodoro_time = int(self.controller.pomodoro.get())
                self.current_time.set(f"{pomodoro_time:02d}:00")
            elif next_up == "Short Break":
                short_break_time = int(self.controller.short_break.get())
                self.current_time.set(f"{short_break_time:02d}:00")
            elif next_up == "Long Break":
                long_break_time = int(self.controller.long_break.get())
                self.current_time.set(f"{long_break_time:02d}:00")
            # go fo next round in the deque
            self._timer_decrement_job = self.after(1000, self.decrement_timer)

    def start_timer(self):
        self.timer_running = True
        self.start_button["state"] = "disabled"
        self.stop_button["state"] = "enabled"
        self.decrement_timer()

    def stop_timer(self):
        self.timer_running = False
        self.start_button["state"] = "enabled"
        self.stop_button["state"] = "disabled"
        if self._timer_decrement_job:
            self.after_cancel(self._timer_decrement_job)
            self._timer_decrement_job = None

    def reset_timer(self):
        self.stop_timer()
        pomodoro_time = int(self.controller.pomodoro.get())
        self.current_time.set(f"{pomodoro_time:02d}:00")
        self.controller.timer_schedule = deque(self.controller.timer_order)
        self.current_timer_label.set(self.controller.timer_schedule[0])



