# Import Relevant Libraries here
import tkinter as tk
from tkinter import messagebox, font

"""Class to handle Device Restart and SystemD Services"""
class SystemSettings(tk.Toplevel):
    def __init__(self, transport):
        super().__init__()
        self.transient()  # make window transient to its master
        self.grab_set()   # grab the focus
        self.lift()       # bring the window to the front

        self.title("System Information")
        self.geometry("640x480")
        self.transport = transport

        # Define some font styles
        self.header_font = font.Font(size=16, weight="bold")
        self.label_font = font.Font(size=12)
        self.info_font = font.Font(size=10)

        self.create_widgets()

    def create_widgets(self):

        # Main header
        self.header_label = tk.Label(self, text="System Reboot", font=self.header_font)
        self.header_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))#

        # Software Restart Button
        self.send_button = tk.Button(self, text="Software Restart", state=tk.NORMAL, command=self.software_restart)
        self.send_button.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        # Hardware Restart Button
        self.send_button = tk.Button(self, text="Hardware Restart", state=tk.NORMAL, command=self.hardware_restart)
        self.send_button.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        # Instruction label
        self.instruction_label = tk.Label(self, text="To perform a software restart, please press the software restart button.", font=self.label_font)
        self.instruction_label.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")

        # Text Information Label
        self.information_label = tk.Label(self, text = "To perform a hardware restart, please press the hardware restart button.\n", font = self.label_font)
        self.information_label.grid(row = 2, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")

        # Spacer between buttons
        self.spacer_label = tk.Label(self, height=2)  # Empty label to give some space between widgets
        self.spacer_label.grid(row=5, column=0, columnspan=2)
    
    # This function hasn't been done yet
    def software_restart(self):
        print("Restarting services on the device\n")
        messagebox.showinfo("Software Restart", "Software restart command sent to device")
        ssh = self.transport.open_session()
        cmd = 'sudo systemctl restart PiMeter.service'
        ssh.exec_command(cmd)
        

    # This function sends a hardware restart command to the Pis
    def hardware_restart(self):
        print("Hardware restarting the raspberry pi\n")  
        messagebox.showinfo("Hardware Restart", "Hardware restart command sent to device")  
        ssh = self.transport.open_session()
        cmd = 'sudo reboot now'
        ssh.exec_command(cmd)
