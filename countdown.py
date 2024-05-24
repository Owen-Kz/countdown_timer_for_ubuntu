import tkinter as tk
from tkinter import font
import time
from threading import Thread

class CountdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer")
        self.time_in_seconds = 0
        self.running = False
        self.paused = False
        self.clicked_section = None
        self.is_fullscreen = False
        self.bg_color = '#333'
        self.root.configure(bg=self.bg_color)

        # Custom font settings
        self.custom_font = font.Font(family="Helvetica", size=500, weight="bold")
        self.small_font = font.Font(family="Helvetica", size=20)

        self.time_label = tk.Label(root, text="00:00", font=self.custom_font, fg="white", bg=self.bg_color)
        self.time_label.pack(expand=True)

        self.message_label = tk.Label(root, text="", font=self.small_font, fg="white", bg=self.bg_color)
        self.message_label.pack()

        self.root.bind("<Up>", self.increase_time)
        self.root.bind("<Down>", self.decrease_time)
        self.root.bind("<space>", self.toggle_timer)
        self.root.bind("<Delete>", self.reset_timer)
        self.root.bind("<Escape>", self.exit_or_windowed)
        self.time_label.bind("<Button-1>", self.click_time)
        self.root.bind("<Double-Button-1>", self.toggle_fullscreen)
        # self.time_label.bind("<Double-Button-1>", self.toggle_fullscreen)
        self.root.bind("<Configure>", self.resize_text)  # Bind the resize event

        self.update_time_label()

    def increase_time(self, event=None):
        if self.clicked_section == "hours":
            self.time_in_seconds += 3600
        elif self.clicked_section == "mins":
            self.time_in_seconds += 60
        elif self.clicked_section == "secs":
            self.time_in_seconds += 1
        else:
            self.time_in_seconds += 60
        self.update_time_label()

    def decrease_time(self, event=None):
        if self.clicked_section == "hours" and self.time_in_seconds >= 3600:
            self.time_in_seconds -= 3600
        elif self.clicked_section == "mins" and self.time_in_seconds >= 60:
            self.time_in_seconds -= 60
        elif self.clicked_section == "secs" and self.time_in_seconds >= 1:
            self.time_in_seconds -= 1
        else:
            if self.time_in_seconds >= 60:
                self.time_in_seconds -= 60
        self.update_time_label()

    def toggle_timer(self, event=None):
        if not self.running and not self.paused:
            self.start_countdown()
        elif self.paused:
            self.paused = False
            self.message_label.config(text="")
        else:
            self.paused = True
            self.message_label.config(text="Paused", fg="white")

    def reset_timer(self, event=None):
        self.running = False
        self.paused = False
        self.time_in_seconds = 0
        self.update_time_label()
        self.message_label.config(text="")
        # Reset background color to original when timer is reset
        self.bg_color = '#333'
        self.time_label.configure(bg=self.bg_color)
        self.message_label.configure(bg=self.bg_color)
        self.root.configure(bg=self.bg_color)

    def exit_or_windowed(self, event=None):
        if self.is_fullscreen:
            self.toggle_fullscreen()
        else:
            self.root.quit()

    def update_time_label(self):
        if self.time_in_seconds >= 3600:  # If time is more than or equal to 1 hour
            hours, remainder = divmod(self.time_in_seconds, 3600)
            mins, secs = divmod(remainder, 60)
            time_str = f'{hours:02d}:{mins:02d}:{secs:02d}'
        else:
            mins, secs = divmod(self.time_in_seconds, 60)
            time_str = f'{mins:02d}:{secs:02d}'
        self.time_label.config(text=time_str, fg="white")
        self.root.update()

    def start_countdown(self):
        self.running = True
        def run():
            while self.running:
                if self.paused:
                    time.sleep(1)
                    continue
                if self.time_in_seconds > 0:
                    time.sleep(1)
                    self.time_in_seconds -= 1
                    self.update_time_label()
                if self.time_in_seconds == 0:
                    self.running = False
                    self.bg_color = 'red'
                    self.time_label.config(text="TIME'S UP!", fg="white", bg=self.bg_color)
                    self.message_label.config(text="Press 'DEL' button to reset time", fg="white", bg=self.bg_color)
                    self.root.configure(bg=self.bg_color)
                    break
        Thread(target=run).start()

    def click_time(self, event):
        x = event.x
        time_label_width = self.time_label.winfo_width()
        # Determine if the click was on the hours, minutes, or seconds part
        if self.time_in_seconds >= 3600:  # If displaying hours
            if x < time_label_width / 3:
                self.clicked_section = "hours"
            elif x < 2 * time_label_width / 3:
                self.clicked_section = "mins"
            else:
                self.clicked_section = "secs"
        else:
            if x < time_label_width / 2:
                self.clicked_section = "mins"
            else:
                self.clicked_section = "secs"
        # print(f"Clicked on {self.clicked_section}")

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)
        if not self.is_fullscreen:
            self.root.geometry("800x400")

    def resize_text(self, event=None):
        # Calculate font size based on window size
        width, height = self.root.winfo_width(), self.root.winfo_height()
        new_font_size = min(max(int(height / 5), 10), 500)  # Dynamic font size calculation
        self.custom_font.configure(size=new_font_size)
        self.time_label.configure(font=self.custom_font)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1920x1080")  # Set the window size
    app = CountdownApp(root)
    root.mainloop()
