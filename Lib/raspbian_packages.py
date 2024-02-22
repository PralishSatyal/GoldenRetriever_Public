# Import Relevant Libraries Here
import tkinter as tk
from tkinter import filedialog, messagebox, font
import paramiko
from Lib.utils import read_file
import time

"""Class to Handle Installation of Relevant Raspbian Packages"""
class RaspbianPackages(tk.Toplevel):

    def __init__(self, transport):
        super().__init__()
        self.transient()
        self.lift()

        self.title("Raspbian Packages")
        self.geometry("640x480")
        
        self.transport = transport
        self.file_path = None
        self.connected_username = read_file("login.txt")
        
        # Define some font styles
        self.header_font = font.Font(size=16, weight="bold")
        self.label_font = font.Font(size=12)
        self.info_font = font.Font(size=10)

        self.create_widgets() 
        self.pip_requirements = f"Metering Software for the Raspberry pi/Requirements/requirements.txt"

    # Function to create widgets for VPN
    def create_widgets(self):
        self.json_select_button = tk.Button(self, text="Select package requirements file", command=self.select_file)
        self.json_select_button.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.send_button = tk.Button(self, text="Send installation packages", state=tk.DISABLED, command=self.send_file)
        self.send_button.grid(row=5, column=1, padx=10, pady=10, sticky="e")

        # Main header
        self.header_label = tk.Label(self, text="Raspbian Packages Manager", font=self.header_font)
        self.header_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        # Instruction label
        self.instruction_label1 = tk.Label(self, text="Select the requirements.sh script to be sent to the device\n", font=self.label_font)
        self.instruction_label1.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")

        # Text Information Label
        self.information_label1 = tk.Label(self, text = "In this version, ensure you have the static filename as 'requirements.sh'\n", font = self.info_font)
        self.information_label1.grid(row = 3, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")

        self.information_label2 = tk.Label(self, text = "Once sent to the device, the device will run all shell commands from the requirements.sh file.\n Expect to lose device connectivity for 5 minutes.\nThis is because the device will reboot as instructed in the script.\n", font = self.info_font)
        self.information_label2.grid(row = 4, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")

        # Spacer between buttons
        self.spacer_label = tk.Label(self, height=2)  # Empty label to give some space between widgets
        self.spacer_label.grid(row=5, column=0, columnspan=2)


    # Function to select file for package installation
    def select_file(self):
        self.file_path = filedialog.askopenfilename()

        # If file has been selected 
        if self.file_path:
            self.send_button.config(state=tk.NORMAL)

    # Function to send SH file to the Pi
    def send_file(self):
        if not self.transport or not self.transport.is_active():
            messagebox.showerror("Error", "Not connected to Raspberry Pi.")
            return

        try:
            sftp = paramiko.SFTPClient.from_transport(self.transport)
            remote_dir = f"/home/{self.connected_username}/PiMeter/Lib/Azure_Connection/"

            package_remote_path = remote_dir + self.file_path.split("/")[-1]
            requirements_remote_path = remote_dir + self.pip_requirements.split("/")[-1]

            print(f"The package remote path is : {package_remote_path}")
            print(f"The pip requirements file is stored at : {requirements_remote_path}")

            sftp.put(self.file_path, package_remote_path)
            sftp.put(self.pip_requirements, requirements_remote_path)

            # Install dos2unix on the pi
            ssh = self.transport.open_session()
            cmd1 = 'sudo apt-get install dos2unix'
            ssh.exec_command(cmd1)
            print("Trying to install dos2unix")
            time.sleep(2)
            ssh.close()

            # Convert the relevant scripts that are sent to the pi
            ssh = self.transport.open_session()
            print("Running command 2")
            cmd2 = f'dos2unix {package_remote_path} && dos2unix {requirements_remote_path}' 
            ssh.exec_command(cmd2)
            time.sleep(1)
            print("Converting requirements script via dos2unix")
            ssh.close()

            # Make the script executable
            ssh = self.transport.open_session()
            print("Running command 3")
            cmd3 = f'sudo chmod +x {package_remote_path} && sudo {package_remote_path}'
            ssh.exec_command(cmd3)
            print("Sent command 3")
            ssh.recv_exit_status()
            time.sleep(1)
            print("Trying to exec the requirements file then run installation script")


            messagebox.showinfo("Success", "File sent and executed successfully.")
            time.sleep(3)

            sftp.close()
            ssh.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))