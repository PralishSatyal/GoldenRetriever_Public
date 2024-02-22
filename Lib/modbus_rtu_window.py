# Import Relevent Libraries
import tkinter as tk
from tkinter import messagebox
import paramiko
from Lib.slave_packer import SlavePacker

"""Class to show Modbus Window Information"""
class ModbusRTU(SlavePacker):

    def __init__(self, transport):
        # Initialisation of the parent class
        super().__init__(transport)  

        # Modbus RTU Specifics
        self.title("Modbus RTU")
        self.geometry('840x920')
        self.mode = 'RTU'

    # Method of creating RTU Specific Widgets
    def create_rtu_widgets(self):
        self.rtu_frame = tk.Frame(self)
        self.rtu_frame.grid (row = 1, column = 0, padx = 5, pady = 5, sticky = "ew")

    # Method for sending configuration to the device
    def send_configuration(self):
        print("Sending RTU Configuration to device")
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
                        "port": slave['port_combobox'].get(),
                        "slave_id": slave['slave_id_entry'].get(),
                        "baud_rate": slave['baud_combobox'].get(),
                        "data_bits": slave['bits_combobox'].get(),
                        "parity": slave['parity_combobox'].get(),
                        "stop_bits": slave['stop_bits_combobox'].get(),
                        "time_out": slave['time_out_entry'].get(),
                        "modbus_map": slave["file_path"].split("/")[-1]
                    }

                    slave_data_list.append(slave_data)

            config_data = {
                "modbus_type": "RTU",
                "slaves": slave_data_list
            }

            return config_data

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Function to return btoh configurations
    def get_configuration(self):
        return self.send_configuration()
