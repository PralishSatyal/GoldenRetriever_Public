# Import Relevant Libraries
import tkinter as tk
from tkinter import Scrollbar

"""Class to show data from Prime Software service"""
class DataView(tk.Toplevel):

    def __init__(self, transport):
        super().__init__()
        self.transient()
        # self.grab_set()
        self.lift()
        
        self.title("Live Data View")
        self.geometry("800x500")

        self.transport = transport
        self.fetching = False  # To keep track if logs are being fetched

        self.create_widgets()

    def create_widgets(self):
        self.modbus_select_button = tk.Button(self, text="View Live Data", command=self.start_viewing_data)
        self.modbus_select_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.stop_fetching_button = tk.Button(self, text="Stop Fetching", command=self.stop_viewing_data)
        self.stop_fetching_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.clear_output_button = tk.Button(self, text="Clear Output", command=self.clear_output)
        self.clear_output_button.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        self.csv_display = tk.Text(self, wrap=tk.NONE, height=20, width=60)  # wrap=tk.NONE allows horizontal scrolling
        self.csv_display.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Adding a vertical scrollbar to the Text widget
        self.vertical_scroll = Scrollbar(self, command=self.csv_display.yview)
        self.vertical_scroll.grid(row=1, column=3, sticky="ns")
        self.csv_display.config(yscrollcommand=self.vertical_scroll.set)

        # Adding a horizontal scrollbar to the Text widget
        self.horizontal_scroll = Scrollbar(self, command=self.csv_display.xview, orient=tk.HORIZONTAL)
        self.horizontal_scroll.grid(row=2, column=0, columnspan=3, sticky="ew")
        self.csv_display.config(xscrollcommand=self.horizontal_scroll.set)

    def start_viewing_data(self):
        self.fetching = True
        self.poll_logs()

    def stop_viewing_data(self):
        self.fetching = False

    def clear_output(self):
        self.csv_display.delete('1.0', tk.END)

    def poll_logs(self):
        if not self.fetching:
            return

        cmd = 'journalctl -u PiMeter.service -n 10'
        ssh = self.transport.open_session()
        ssh.exec_command(cmd)
        
        output = ssh.recv(1024).decode('utf-8')
        while True:
            more_output = ssh.recv(1024).decode('utf-8')
            if not more_output:
                break
            output += more_output

        self.csv_display.delete('1.0', tk.END)
        self.csv_display.insert(tk.END, output)
        ssh.close()

        self.after(1000, self.poll_logs)
