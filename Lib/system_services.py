# Import Relevant Libraries here
import tkinter as tk
from tkinter import messagebox, font, scrolledtext

# Import custom utility module
from Lib.utils import read_file


"""Class to handle System Services"""
class SystemServices(tk.Toplevel):

    def __init__(self, transport):
        super().__init__()
        self.transient()  # make window transient to its master
        # self.grab_set()   # grab the focus
        self.lift()       # bring the window to the front

        self.title("System Information")
        self.geometry("900x640")
        self.transport = transport
        self.connected_username = read_file("login.txt")

        # Define some font styles
        self.header_font = font.Font(size=16, weight="bold")
        self.label_font = font.Font(size=12)
        self.info_font = font.Font(size=10)
        
        self.create_widgets()


    def create_widgets(self):
        
        # Main header
        self.header_label = tk.Label(self, text="System Service Setup", font=self.header_font)
        self.header_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        # Software Service Setup
        self.service_button = tk.Button(self, text="Software Service Setup", state=tk.NORMAL, command=self.software_service_setup)
        self.service_button.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        # VPN Service Setup
        self.vpn_button = tk.Button(self, text="VPN Service Setup", state=tk.NORMAL, command=self.vpn_service_setup) 
        self.vpn_button.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        # Instruction label
        self.instruction_label = tk.Label(self, text="To setup the VPN service and the Software service, please press the buttons below.", font=self.label_font)
        self.instruction_label.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")

        # Text Information Label
        self.information_label = tk.Label(self, text = "Once these services are created, it is advised to perform a hardware reboot.\nAfter this, the services should be working\n", font = self.info_font)
        self.information_label.grid(row = 3, column=0, columnspan=4, padx=30, pady=(0, 30), sticky="w")

        # Spacer between buttons
        self.spacer_label = tk.Label(self, height=2)
        self.spacer_label.grid(row=5, column=0, columnspan=2)

        # Text widget for displaying command outputs
        self.output_text = scrolledtext.ScrolledText(self, width=100, height=15, wrap = tk.NONE)
        self.output_text.grid(row=6, column=0, columnspan=3, padx=20, pady=20)

        # Horizontal scrollbar
        self.hscroll = tk.Scrollbar(self, orient='horizontal', command=self.output_text.xview)
        self.hscroll.grid(row=7, column=0, columnspan=3, sticky='ew')
        self.output_text['xscrollcommand'] = self.hscroll.set
        
        # Button to fetch Raspberry Pi temperature
        self.temp_button = tk.Button(self, text="Get RPi Temperature", command=self.get_temp)
        self.temp_button.grid(row=8, column=0, padx=10, pady=10, sticky="w")
        
        # Button to fetch service statuses
        self.status_button = tk.Button(self, text="Get Service Statuses", command=self.get_services_status)
        self.status_button.grid(row=8, column=1, padx=10, pady=10, sticky="w")
        
        # Button to clear the text widget
        self.clear_button = tk.Button(self, text="Clear Output", command=self.clear_output)
        self.clear_button.grid(row=8, column=2, columnspan=2, padx=10, pady=10, sticky = 'w')


    
    def software_service_setup(self):
        print("Setting up the PiMeter service so code runs on boot\n")
        
        # Commands to execute
        commands = [
            f'''echo "[Unit]
    Description=PiMeter Service
    After=multi-user.target

    [Service]
    Type=idle
    ExecStart=/usr/bin/python3 /home/{self.connected_username}/PiMeter/main.py
    WorkingDirectory=/home/{self.connected_username}/PiMeter/
    User={self.connected_username}

    [Install]
    WantedBy=multi-user.target" | sudo tee /lib/systemd/system/PiMeter.service''',
            
            "sudo chmod 644 /lib/systemd/system/PiMeter.service",
            "sudo systemctl daemon-reload",
            "sudo systemctl enable PiMeter.service",
            "sudo systemctl start PiMeter.service"
        ]
        
        # Execute the commands
        for cmd in commands:
            ssh_channel = self.transport.open_channel("session")
            if not ssh_channel.active:
                print("Failed to open an SSH channel.")
                return

            ssh_channel.exec_command(cmd)
            stdout = ssh_channel.makefile('r', -1)
            stderr = ssh_channel.makefile_stderr('r', -1)
            print(stdout.read())
            print(stderr.read())
            ssh_channel.close()
        
        messagebox.showinfo("System Service", "Succesfully enabled software to start on boot")
    
    # New function to fetch Raspberry Pi temperature
    def get_temp(self):
        cmd = "date '+%Y-%m-%d %H:%M:%S'; vcgencmd measure_temp"
        output = self.execute_ssh_command(cmd)
        formatted_output = " ".join(output.split("\n"))  
        self.output_text.insert(tk.END, formatted_output + "\n" + "="*50 + "\n")  # Separating outputs by lines

    # New function to fetch the status of services
    def get_services_status(self):
        services = ["PiMeter.service", "ovpn.service"]
        for service in services:
            cmd = f"sudo systemctl status {service}"
            output = self.execute_ssh_command(cmd)
            self.output_text.insert(tk.END, output + "\n" + "="*50 + "\n")  # Separating outputs by line


    # New function to clear the Text widget
    def clear_output(self):
        self.output_text.delete(1.0, tk.END)  # Clears the text widget

    # A helper function to execute SSH commands and return their output
    def execute_ssh_command(self, cmd):
        try:
            ssh_channel = self.transport.open_channel("session")
            if not ssh_channel.active:
                print("Failed to open an SSH channel.")
                return

            ssh_channel.exec_command(cmd)
            stdout = ssh_channel.makefile('r', -1)
            stderr = ssh_channel.makefile_stderr('r', -1)
            result = stdout.read() + stderr.read()
            ssh_channel.close()

            return result.decode('utf-8')

        except Exception as e:
            return str(e)

    def vpn_service_setup(self):
        # Placeholder function for setting up the VPN service (note the static VPN detail and the Static PI username detail and the static filename
        print("Setting up the VPN service so code runs on boot\n")
        
        # Commands to execute
        commands = [
            f'''echo "[Unit]
    Description=VPN Service
    After=multi-user.target

    [Service]
    Type=idle
    ExecStart=/home/{self.connected_username}/PiMeter/Lib/Azure_Connection/ovpn.sh
    WorkingDirectory=/home/{self.connected_username}/PiMeter/Lib/Azure_Connection/
    User={self.connected_username}

    [Install]
    WantedBy=multi-user.target" | sudo tee /lib/systemd/system/ovpn.service''',
            f"sudo dos2unix /home/{self.connected_username}/PiMeter/Lib/Azure_Connection/ovpn.sh",
            "sudo chmod 644 /lib/systemd/system/ovpn.service",
            "sudo systemctl daemon-reload",
            "sudo systemctl enable ovpn.service",
            "sudo systemctl start ovpn.service",
        ]

        # Execute the commands
        for cmd in commands:
            ssh_channel = self.transport.open_channel("session")
            if not ssh_channel.active:
                print("Failed to open an SSH channel.")
                return

            ssh_channel.exec_command(cmd)
            stdout = ssh_channel.makefile('r', -1)
            stderr = ssh_channel.makefile_stderr('r', -1)
            print(stdout.read())
            print(stderr.read())
            ssh_channel.close()
        
        messagebox.showinfo("System Service", "Succesfully enabled vpn to start on boot")
    