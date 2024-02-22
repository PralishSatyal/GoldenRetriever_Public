# Import Relevant Libraries
import tkinter as tk
from tkinter import filedialog, messagebox, font
import paramiko
import os
from Lib.utils import read_file

"""Class to handle OpenVPN window"""
class OpenVpnWindow(tk.Toplevel):

    def __init__(self, transport):
        super().__init__()
        self.transient()
        self.lift()
        
        self.title("Open VPN Configuration")
        self.geometry("640x480")
        
        self.transport = transport
        self.connected_username = read_file("login.txt")
        self.file_path = None
        
        # Define some font styles
        self.header_font = font.Font(size=16, weight="bold")
        self.label_font = font.Font(size=12)
        self.info_font = font.Font(size=10)
        
        self.create_widgets()

    def create_widgets(self):
        # Main header
        self.header_label = tk.Label(self, text="OpenVPN Configuration", font=self.header_font)
        self.header_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        # Instruction label
        self.instruction_label = tk.Label(self, text="Please select your OpenVPN (.ovpn) configuration file to upload.", font=self.label_font)
        self.instruction_label.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")

        # Text Information Label
        self.information_label = tk.Label(self, text = "By selecting your open VPN file, a shell script will be automatically generated\n which will be called to run on startup. This means that the VPN connection will be kept \nalive forever as long as the Device is powered on.\n", font = self.info_font)
        self.information_label.grid(row = 3, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")
        
        # File select button
        self.json_select_button = tk.Button(self, text="Select OpenVPN (.ovpn) file", command=self.select_file, width=30)
        self.json_select_button.grid(row=5, column=0, padx=(20, 10), sticky="w")

        # Send button
        self.send_button = tk.Button(self, text="Send VPN files", state=tk.DISABLED, command=self.send_file, width=20)
        self.send_button.grid(row=5, column=1, padx=(0, 20), sticky="e")

        # Spacer between buttons
        self.spacer_label = tk.Label(self, height=2)  # Empty label to give some space between widgets
        self.spacer_label.grid(row=5, column=0, columnspan=2)

    # Function to select file for VPN
    def select_file(self):
        self.file_path = filedialog.askopenfilename()

        # If file has been selected 
        if self.file_path:
            self.send_button.config(state=tk.NORMAL)

    # Function to generate relevant script based on VPN filename
    def generate_vpn_sh(self):
        print("Generating sh file from VPN filename")
        with open('ovpn.sh', "w") as f:
            f.write("#!/bin/sh\n")
            f.write(f"""\necho 'Starting OpenVPN Connection to Azure'\nsudo openvpn --config /home/{self.connected_username}/PiMeter/Lib/Azure_Connection/*.ovpn""") # fix this?
        print(f"Finished creating shell file")
        self.convert_line_endings('ovpn.sh')

    # Function to delete local instance of VPN connection script
    def delete_vpn_sh(self):
        print("Deleting previously generated local sh file\n")
        os.remove('ovpn.sh')
        print("VPN file succesfully removed from local store\n")

    # Function to send OVPN file(s) to the Pi
    def send_file(self):
        if not self.transport or not self.transport.is_active():
            messagebox.showerror("Error", "Not connected to Raspberry Pi.")
            return
        try:

            self.generate_vpn_sh()

            sftp = paramiko.SFTPClient.from_transport(self.transport)  # This is the correct way to initiate SFTP
            remote_dir = f"/home/{self.connected_username}/PiMeter/Lib/Azure_Connection/"  

            # Send the VPN file
            vpn_remote_path = remote_dir + self.file_path.split("/")[-1]
            print(f"The VPN remote path is : {vpn_remote_path}")
            sftp.put(self.file_path, vpn_remote_path)
            
            # Need to send the Generated SH file corresponding to that vpn
            sh_remote_path = remote_dir + 'ovpn.sh'
            print(f"The shell remote path is : {sh_remote_path}")
            sftp.put('ovpn.sh', sh_remote_path)

            # Need to ensure that the SH file is made executable 
            ssh = self.transport.open_session()
            cmd = f'sudo chmod +x {sh_remote_path}'
            ssh.exec_command(cmd)

            sftp.close()
            self.delete_vpn_sh()
            ssh.close()

            messagebox.showinfo("Success", "File sent successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def convert_line_endings(self, filepath):
        """
        Convert a file's line endings from Windows-style (CRLF) to Unix-style (LF).
        
        Args:
        - filepath (str): The path to the file to be converted.
        """
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()

        # Replace Windows line endings with Unix line endings
        content = content.replace('\r\n', '\n')

        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)