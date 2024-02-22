# Import Relevent Libraries
import tkinter as tk
from tkinter import filedialog, messagebox
import os

# Import custom utility module
from Lib.utils import read_file

"""Class to show Modbus Window Information"""
class ModbusMap(tk.Toplevel):

    def __init__(self, transport):
        super().__init__()
        self.transient()
        self.lift()
        
        self.title("Modbus Map")
        self.geometry("840x640")

        self.transport = transport
        self.connected_username = read_file("login_details.txt")[0]
        self.file_path = None

        self.remote_dir = f"/home/{self.connected_username}/PiMeter/modbus_dir/"
        self.config_path = f"/home/{self.connected_username}/PiMeter/config/config.json"


    def create_widgets(self):
        self.initialise_widgets()

    def send_configuration(self):
        # Default behavior. Can be empty or a print statement for debug.
        print("Default send configuration from ModbusMap class.")


    def initialise_widgets(self, frame, slave=None):
        csv_display = tk.Text(frame, wrap=tk.WORD, height=20, width=60)
        csv_display.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        modbus_select_button = tk.Button(frame, text="Select Modbus Map file", command=lambda: self.select_file(frame))
        modbus_select_button.grid(row=3, column=0, padx=5, pady=5, sticky="w")       

        # Use a lambda to determine the target when saving.
        save_button = tk.Button(frame, text="Save Edited Map", command=lambda s=slave: self.save_edits(s))
        save_button.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        return csv_display


    def select_file(self, slave_frame=None):
        file_path_temp = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
            
        if file_path_temp:
            if slave_frame:
                slave = next((s for s in self.slaves if s["frame"] == slave_frame), None)
                if slave:
                    slave["file_path"] = file_path_temp  
                    with open(file_path_temp, "r") as file:
                        csv_content = file.read()
                        slave['csv_display'].delete(1.0, tk.END)
                        slave['csv_display'].insert(tk.END, csv_content)
            else:
                self.file_path = file_path_temp
                with open(file_path_temp, "r") as file:
                    csv_content = file.read()
                    self.csv_display.delete(1.0, tk.END)
                    self.csv_display.insert(tk.END, csv_content)

                self.send_button.config(state = tk.NORMAL)

    # Method to save edits per slave. Default state is with no slaves
    def save_edits(self, slave=None):
        if slave:
            target_display = slave['csv_display']
            target_file_path = slave['file_path']
        else:
            target_display = self.csv_display
            target_file_path = self.file_path

        if not target_file_path:
            messagebox.showerror("Error", "No file is selected.")
            return

        try:
            with open(target_file_path, 'w') as file:
                edited_content = target_display.get(1.0, tk.END)
                file.write(edited_content)
            messagebox.showinfo("Success", "Modbus map edited and saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_modbus_map(self):
        print("Deleting any other modbus maps on device\n")
        ssh = self.transport.open_session()
        cmd = 'sudo rm ' + self.remote_dir + '*'
        ssh.exec_command(cmd)
        print("Removed any modbus maps on device\n")
        ssh.close()

    def delete_temp_json(self):
        print("Deleting temp json store\n")
        try:
            os.remove("temp_config.json")
            print("Successfully removed local json store\n")
        except:
            print("Local JSON file could not be removed")
