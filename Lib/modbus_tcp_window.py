# Import Relevant Libraries
import tkinter as tk
from tkinter import messagebox
import paramiko
from Lib.slave_packer import SlavePacker

"""Class to show Modbus Window Information"""
class ModbusTCP(SlavePacker):
    
    def __init__(self, transport):
        # Initialisation of the parent class
        super().__init__(transport)
        
        # Modbus TCP Widgets
        self.title("Modbus TCP")
        self.geometry("840x640")
        self.mode = 'TCP'

    # Method for creating widgets
    def create_tcp_widgets(self):
        self.tcp_frame = tk.Frame(self)
        self.tcp_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

    # Function to send configuration to device
    def send_configuration(self):
        print("Sending TCP Configuration to device")
        if not self.transport or not self.transport.is_active():
            messagebox.showerror("Error", "Not connected to Raspberry Pi.")
            return

        try:
            print("Starting the SFTP client for sending files")
            sftp = paramiko.SFTPClient.from_transport(self.transport)

            slave_data_list = []

            for slave in self.slaves:
                if slave["file_path"]:
                    modbus_remote_path = self.remote_dir + slave["file_path"].split("/")[-1]
                    sftp.put(slave["file_path"], modbus_remote_path)
                    
                    slave_data = {
                        "ip_address": slave['ip_address_entry'].get(),
                        "slave_id": slave['slave_id_entry'].get(),
                        "modbus_map": slave["file_path"].split("/")[-1]
                    }

                    slave_data_list.append(slave_data)

            config_data = {
                "modbus_type": "TCP",
                "slaves": slave_data_list
            }

            return config_data

        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    # Function to get ModbusTCP and ModbusRTU classes:
    def get_configuration(self):
        return self.send_configuration()
