import tkinter as tk
from tkinter import messagebox
import paramiko

import json
import os

from Lib.utils import read_file
from Lib.modbus_rtu_window import ModbusRTU
from Lib.modbus_tcp_window import ModbusTCP

class MainController(tk.Toplevel):

    def __init__(self, transport):
        super().__init__()
        
        self.title("Modbus Configuration")
        self.geometry('400x200')
        
        self.transport = transport
        self.connected_username = read_file("login.txt")[0] 

        self.send_button = tk.Button(self, text="Send Combined Configuration", command=self.send_combined_configuration)
        self.send_button.pack(pady=20)

        self.open_tcp = tk.Button(self, text = "Open TCP Config Window", command = self.open_tcp_window)
        self.open_tcp.pack(pady = 20)

        self.open_rtu = tk.Button(self, text = "Open RTU Window", command = self.open_rtu_window)
        self.open_rtu.pack(pady = 20)

        self.modbus_tcp = None
        self.modbus_rtu = None

    # Function to open TCP Window
    def open_tcp_window(self):
        self.modbus_tcp = ModbusTCP(self.transport)
        self.modbus_tcp.create_tcp_widgets()
        print("Created TCP Widgets")
    
    # Function to open RTU Window
    def open_rtu_window(self):
        self.modbus_rtu = ModbusRTU(self.transport)
        self.modbus_rtu.create_rtu_widgets()
        print("Created RTU Widgets")

    # Option to send combined config json
    def send_combined_configuration(self):
        tcp_config = self.modbus_tcp.get_configuration() if self.modbus_tcp else None
        rtu_config = self.modbus_rtu.get_configuration() if self.modbus_rtu else None

        combined_config = []
        if tcp_config:
            combined_config.append(tcp_config)
        if rtu_config:
            combined_config.append(rtu_config)

        # If no configuration, return an error
        if not combined_config:
            messagebox.showerror("Error", "No configuration available to send.")
            return
        try:
            if not self.transport or not self.transport.is_active():
                messagebox.showerror("Error", "Not connected to Raspberry Pi.")
                return
            
            sftp = paramiko.SFTPClient.from_transport(self.transport)
            
            with open('config.json', 'w') as temp_config_file:
                json.dump(combined_config, temp_config_file)
            
            remote_path = f"/home/{self.connected_username}/PiMeter/config/config.json"
            sftp.put('config.json', remote_path)
            sftp.close()
            os.remove('config.json') # remove the local copy for decluttering
            
            messagebox.showinfo("Success", "Combined configuration sent successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

