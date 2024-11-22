import psutil
import tkinter as tk
from tkinter import ttk

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Task Manager")

        # Create a frame for CPU usage
        self.cpu_frame = ttk.LabelFrame(root, text="CPU Usage")
        self.cpu_frame.pack(padx=10, pady=10, fill="both", expand="yes")

        # Create a label to display CPU usage
        self.cpu_label = ttk.Label(self.cpu_frame, text="CPU Usage: 0%", font=("Arial", 24))
        self.cpu_label.pack(padx=10, pady=10)

        # Create a treeview for processes
        self.process_frame = ttk.LabelFrame(root, text="Running Processes")
        self.process_frame.pack(padx=10, pady=10, fill="both", expand="yes")

        self.process_tree = ttk.Treeview(self.process_frame, columns=("PID", "Name", "CPU", "Memory"), show='headings')
        self.process_tree.heading("PID", text="PID")
        self.process_tree.heading("Name", text="Name")
        self.process_tree.heading("CPU", text="CPU (%)")
        self.process_tree.heading("Memory", text="Memory (MB)")

        self.process_tree.pack(padx=10, pady=10, fill="both", expand="yes")

        # Start updating CPU usage and process list
        self.update_cpu_usage()
        self.update_process_list()

    def update_cpu_usage(self):
        # Get the CPU usage percentage
        cpu_usage = psutil.cpu_percent(interval=1)
        self.cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
        self.root.after(1000, self.update_cpu_usage)

    def update_process_list(self):
        # Clear the current process list
        for row in self.process_tree.get_children():
            self.process_tree.delete(row)

        # Get a list of all running processes
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                # Get process info
                pid = proc.info['pid']
                name = proc.info['name']
                cpu = proc.info['cpu_percent']  # This will be 0 initially; use sleep to get real-time data
                memory = proc.info['memory_info'].rss / (1024 * 1024)  # Convert bytes to MB

                # Insert process info into the treeview
                self.process_tree.insert("", "end", values=(pid, name, cpu, round(memory, 2)))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Call this method again after 1 second
        self.root.after(1000, self.update_process_list)

if __name__ == "__main__":
    root = tk.Tk()
    task_manager = TaskManager(root)
    root.mainloop()