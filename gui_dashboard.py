import tkinter as tk
from tkinter import ttk
import threading
from attendance import start_attendance  # Ensure your attendance logic is moved into a function called start_attendance
import os


def run_attendance():
    log_text.insert(tk.END, "[INFO] Starting attendance...\n")
    log_text.see(tk.END)
    start_attendance()
    log_text.insert(tk.END, "[INFO] Attendance session ended.\n")
    log_text.see(tk.END)
    load_today_attendance()

def gui_log_callback(message):
    log_text.insert(tk.END, message + "\n")
    log_text.see(tk.END)

def gui_table_callback(name, timestamp, status):
    table.insert("", "end", values=(name, timestamp, status))
    table.yview_moveto(1)
    
def start_attendance_thread():
    threading.Thread(target=run_attendance, daemon=True).start()

def update_clock():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clock_label.config(text=now)
    window.after(1000, update_clock)

# Create the main GUI window
window = tk.Tk()
window.title("Face Recognition Attendance Dashboard")
window.geometry("800x500")
window.configure(bg="#f2f2f2")

# Title Label
title_label = ttk.Label(window, text="Face Recognition Attendance System", font=("Helvetica", 18, "bold"))
title_label.pack(pady=20)

from datetime import datetime

# Clock Label
clock_label = ttk.Label(window, font=("Helvetica", 14))
clock_label.pack()
update_clock()


# Start Button
start_button = ttk.Button(window, text="Start Attendance", command=start_attendance_thread)
start_button.pack(pady=10)

# Log Frame
log_frame = ttk.LabelFrame(window, text="System Logs")
log_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Treeview Table for Attendance
table_frame = ttk.LabelFrame(window, text="Today's Attendance")
table_frame.pack(fill="both", expand=True, padx=20, pady=10)

# Treeview Table
table = ttk.Treeview(table_frame, columns=("Name", "Time", "Status"), show="headings", height=6)
table.heading("Name", text="Name")
table.heading("Time", text="Time")
table.heading("Status", text="Status")  # Entry / Exit
table.pack(fill="x")
# Log Frame
log_frame = ttk.LabelFrame(window, text="System Logs")
log_frame.pack(fill="both", expand=True, padx=20, pady=10)

log_text = tk.Text(log_frame, height=10, wrap="word", font=("Consolas", 10))
log_text.pack(fill="both", expand=True)

window.mainloop()
