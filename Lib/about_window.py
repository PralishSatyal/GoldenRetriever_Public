# Import Relevent Libraries
import tkinter as tk

"""Class to show information about this software to the User"""
class AboutWindow(tk.Toplevel):

     def __init__(self):
        super().__init__()
        self.transient()
        self.grab_set()
        self.lift()

        self.title("About")
        self.geometry("640x480")
        
        tk.Label(self, text="This software was created to flash Metering Software onto any Raspberry Pi.\n For ease of use, it is recommended to use a Raspberry Pi 4,\n with the 32-bit OS-lite variant of Raspbian\n\nV1.0.0, 2023 (C) Pralish\n").pack(pady=10)
        tk.Label(self, text = "You can load modbus maps in CSV format to set-up TCP and RTU connections with multiple slaves. This can be sent to the device for metering\n").pack(pady=10)
        tk.Label(self, text = "This software works was written by Pralish Satyal. (C) Pralish Satyal 2023, pralishbusiness@gmail.com, www.pralish.com\n").pack(pady=10)
