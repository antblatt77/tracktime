import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk
from pystray import Icon, MenuItem as item


class TrackTimeApp:
    def __init__(self, master):
        self.master = master
        master.title("Tracktime App")
        master.geometry("385x335")
        master.configure(bg="black")

        # Load and display the logo image
        logo_image_path = "static/images/logo.png"
        logo_image = Image.open(logo_image_path)
        self.logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(master, image=self.logo_photo, bg="black")
        logo_label.pack(pady=10)

        # Task name input
        self.task_label = tk.Label(master, text="Task:", bg="black", fg="green")
        self.task_label.pack(pady=5)

        self.task_entry = tk.Entry(master, bg="black", fg="green", insertbackground="green")
        self.task_entry.pack(pady=5)

        # Timer display
        self.timer_var = tk.StringVar()
        self.timer_label = tk.Label(master, textvariable=self.timer_var, bg="black", fg="green", font=("Helvetica", 16))
        self.timer_label.pack(pady=10)

        # Buttons
        self.start_button = tk.Button(master, text=" Start ", command=self.start_timer, bg="green", fg="black")
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(master, text=" Stop ", command=self.stop_timer, state=tk.DISABLED, bg="green", fg="black")
        self.stop_button.pack(pady=5)

        # System tray icon - commented out due to error/bug.
        # icon_image_path = "static/images/favicon.png"
        # icon_image = Image.open(icon_image_path)
        # self.icon_photo = ImageTk.PhotoImage(icon_image)
        # menu = (item('Exit', self.on_exit),)
        # self.system_tray_icon = Icon("name", self.icon_photo, "Title", menu)
        # self.system_tray_icon.run()

        # Variables
        self.start_time = None
        self.is_timer_running = False

    def start_timer(self):
        self.start_time = datetime.now()
        self.is_timer_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.update_timer()

    def stop_timer(self):
        self.is_timer_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        elapsed_time = datetime.now() - self.start_time
        task_name = self.task_entry.get()
        result_str = f"{task_name}\nTime spent: {self.format_time(elapsed_time)}"
        self.timer_var.set(result_str)

    def update_timer(self):
        if self.is_timer_running:
            elapsed_time = datetime.now() - self.start_time
            timer_str = f"Time: {self.format_time(elapsed_time)}"
            self.timer_var.set(timer_str)
            self.master.after(1000, self.update_timer)

    def format_time(self, elapsed_time):
        days, seconds = elapsed_time.days, elapsed_time.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours and days:
            return f"{days}days {hours}hrs {minutes}min {seconds}sec"
        elif hours:
            return f"{hours}hrs {minutes}min {seconds}sec"
        else:
            return f"{minutes}min {seconds}sec"

    def on_exit(self, icon, item):
        icon.stop()
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    # Commented out due to error/bug.
    # root.protocol("WM_DELETE_WINDOW", lambda: root.iconify())  # Minimize to system tray on close
    root.configure(bg="black")
    app = TrackTimeApp(root)
    root.mainloop()
