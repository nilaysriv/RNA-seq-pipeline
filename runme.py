import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
import subprocess
import matplotlib.pyplot as plt

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.fastq_label = tk.Label(self, text="Enter the path to the fastq labeled 1:")
        self.fastq_label.pack()

        self.fastq_entry = tk.Entry(self, width=50)
        self.fastq_entry.pack()

        self.browse_button = tk.Button(self, text="Browse", command=self.browse_fastq)
        self.browse_button.pack()

        self.thread_count_label = tk.Label(self, text="Enter the thread count:")
        self.thread_count_label.pack()

        self.thread_count_entry = tk.Entry(self, width=10)
        self.thread_count_entry.pack()

        self.run_button = tk.Button(self, text="Run Script", command=self.run_script)
        self.run_button.pack()

        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack()

        self.status_label = tk.Label(self, text="")
        self.status_label.pack()

        self.visualization_button = tk.Button(self, text="Visualize Output", command=self.visualize_output)
        self.visualization_button.pack()

    def browse_fastq(self):
        filepath = filedialog.askopenfilename(title="Select fastq file")
        self.fastq_entry.delete(0, tk.END)
        self.fastq_entry.insert(0, filepath)

    def run_script(self):
        fastq_path = self.fastq_entry.get()
        thread_count = self.thread_count_entry.get()
        if not fastq_path or not thread_count:
            messagebox.showerror("Error", "Please enter both fastq path and thread count")
            return

        self.status_label.config(text="Running script...")
        self.status_label.update_idletasks()

        command = ["bash", "script.sh"]  # assume your script is named script.sh
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        self.progress_bar.config(mode="indeterminate")
        self.progress_bar.start()

        output, error = process.communicate()

        if process.returncode == 0:
            self.status_label.config(text="Script completed successfully!")
            self.progress_bar.stop()
            self.progress_bar.config(mode="determinate", value=100)
        else:
            self.status_label.config(text="Error running script: " + error.decode())
            self.progress_bar.stop()

    def visualize_output(self):
        # assume the output data is in a file called "counts_data.txt"
        data = []
        with open("data/quant/counts_data.txt", "r") as f:
            for line in f:
                data.append([float(x) for x in line.strip().split()])

        plt.plot(data)
        plt.xlabel("Feature")
        plt.ylabel("Count")
        plt.title("Feature Counts")
        plt.show()

root = tk.Tk()
root.title("RNA-seq Analysis GUI")
app = Application(master=root)
app.mainloop()