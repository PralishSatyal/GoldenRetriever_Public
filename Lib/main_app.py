# Application related Libraries
from tkinter import messagebox, PhotoImage
import tkinter as tk
import webbrowser

# For SSH and OS functions
import paramiko
import os

# Dependent Libraries
from Lib.connection_indicator import ConnectionIndicator
from Lib.openvpn_window import OpenVpnWindow
from Lib.raspbian_packages import RaspbianPackages
from Lib.system_settings import SystemSettings
from Lib.about_window import AboutWindow
from Lib.help_window import HelpWindow
from Lib.mqtt_details import MQTTDetailsWindow
from Lib.file_transfer import FileTransferWindow
from Lib.system_services import SystemServices
from Lib.data_view import DataView
from Lib.main_controller import MainController

from Lib.utils import SimpleCrypt
from cryptography.fernet import Fernet

"""Class for building main GUI with all window dependencies"""
class MainApp:
    def __init__(self, root):
        self.root = root
        img = PhotoImage(file=r'Lib/templates/dog.png')
        self.root.iconphoto(True, img)  # True so that icon is changed for all windows
        self.root.title("Golden Retriever Program")
        self.root.geometry("1280x780")
        
        self.transport = None
        self.create_widgets()
        self.create_menu()

        info_text = tk.Text(self.root, wrap=tk.WORD, height=15, width=100)
        info_text.grid(row=40, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        # Insert text
        info_text.insert(tk.END, "This software package is to flash a Raspberry Pi device with Metering Software and read modbus data.\n\n")
        info_text.insert(tk.END, "Prior to installing the software on a Raspberry Pi device, please make sure you are familiar\nwith the installation steps as outlined in the document")
        info_text.insert(tk.END, "[here]", "link", "\n")
        info_text.insert(tk.END, "\nYou will need to login via SSH to the Pi before you can continue.\n")
        info_text.insert(tk.END, "\nFor more information, please contact Pralish via the contact button.\n")

        # Configure the "link" tag to make it look like a hyperlink
        info_text.tag_configure("link", foreground="blue", underline=True)

        # Bind the click event to the "link" tag to open the local doc file
        info_text.tag_bind("link", "<Button-1>", self.open_doc)
        
        # To make the text widget read-only
        info_text.config(state=tk.DISABLED)

        # Load the login status
        self.load_login_info()
        

    # Function to create widgets, buttons and interface for login screen
    def create_widgets(self):
        self.hostname_label = tk.Label(self.root, text="Raspberry Pi IP:")
        self.hostname_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.hostname_entry = tk.Entry(self.root)
        self.hostname_entry.grid(row=0, column=1, padx=10, pady=10)

        self.username_label = tk.Label(self.root, text="SSH Username:")
        self.username_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=1, column=1, padx=10, pady=10)

        self.password_label = tk.Label(self.root, text="SSH Password:")
        self.password_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.connect_button = tk.Button(self.root, text="Connect", command=self.connect_to_pi)
        self.connect_button.grid(row=1, column=3, padx=10, pady=10)

        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)
        self.password_entry.bind('<Return>', self.connect_to_pi)

        self.disconnect_button = tk.Button(self.root, text="Disconnect", command=self.disconnect_from_pi)
        self.disconnect_button.grid(row=2, column=3, padx=10, pady=10)

        self.connection_status = ConnectionIndicator(self.root, width=20, height=20, bg="lightgrey", highlightthickness=0)
        self.connection_status.grid(row=0, column=3, padx=10, pady=10)

        self.remember_me_var = tk.IntVar() # Check status of checkbox
        self.remember_me_check = tk.Checkbutton(self.root, text="Remember Me", variable=self.remember_me_var)
        self.remember_me_check.grid(row=3, column=1, sticky="w")

    # Function to create primary menu system
    def create_menu(self):
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # File Menu 
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)
        
        file_menu.add_command(label="File Transfer", command=self.open_file_transfer_window)
        file_menu.add_command(label="MQTT Options", command=self.open_mqtt_config_window)
        file_menu.add_command(label="OpenVPN Config", command=self.open_vpn_window)
        file_menu.add_command(label="Package Installer", command=self.open_package_installer_window)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # About Menu 
        about_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label = "Info", menu = about_menu)
        about_menu.add_command(label="About", command=self.open_about_window)
        about_menu.add_command(label="Help", command=self.open_help_window)

        # System Menu
        system_menu =tk.Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label = "System", menu = system_menu)
        system_menu.add_command(label = "Service Menu", command = self.open_service_settings)
        system_menu.add_command(label="Reboot Window", command = self.open_system_settings)

        # Communications Window
        system_menu = tk.Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label = "Communications", menu = system_menu)
        self.menubar.add_command(label = "Modbus Master", command = self.open_modbus_controller)
        system_menu.add_command(label = "Data Viewer", command = self.open_data_window)


    """===========================================Methods for handling connection to device==========================================="""

    # Function to handle connection to the Device
    def connect_to_pi(self, event = None):
        hostname = self.hostname_entry.get().strip()
        username = self.username_entry.get().strip()

        if not hostname or not username:
            messagebox.showerror("Error", "Please enter the Raspberry Pi IP and SSH Username.")
            return

        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Please enter the SSH password.")
            return

        try:
            self.transport = paramiko.Transport((hostname, 22))
            self.transport.connect(username=username, password=password)

            # If Remember Me is checked, write login details to file
            if self.remember_me_var.get():
                crypt = SimpleCrypt()
                encrypted_password = crypt.encrypt(password)
                with open('login_details.txt', 'w') as file:
                    file.write(f"{username}\n{hostname}\n{encrypted_password}")
                with open('.encryption_key.key', 'wb') as key_file:  # Save the key for decryption later
                    key_file.write(crypt.key)

            
            self.disconnect_button.config(state=tk.NORMAL)  # Enable the disconnect button
            self.connect_button.config(state=tk.DISABLED)  # Disable the connect button
            self.connection_status.draw_circle("green")
            messagebox.showinfo("Success", "Connected to Raspberry Pi.")

        except Exception as e:
            self.transport = None
            self.connection_status.draw_circle("red")
            self.connected_username = None # Reset the username if connection resets
            messagebox.showerror("Error", str(e))

    # Function to allow disconnect from the Pi
    def disconnect_from_pi(self):
        if self.transport and self.transport.is_active():

            self.transport.close()
            self.transport = None
            self.connection_status.draw_circle("red")

            # Remove the saved login details on disconnect if Remember Me isn't checked
            if not self.remember_me_var.get() and os.path.exists("login_details.txt"):
                os.remove("login_details.txt")
                os.remove(".encryption_key.key")

            self.connect_button.config(state=tk.NORMAL)
            self.disconnect_button.config(state=tk.DISABLED)
            messagebox.showinfo("Info", "Disconnected from Raspberry Pi.")
            
    # Function for logging into device with encyption key if exists
    def load_login_info(self):
        if os.path.exists("login_details.txt") and os.path.exists(".encryption_key.key"):
            with open('.encryption_key.key', 'rb') as key_file:
                key = key_file.read()
            cipher = Fernet(key)
            with open('login_details.txt', 'r') as file:
                details = file.readlines()
                self.username_entry.insert(0, details[0].strip())
                self.hostname_entry.insert(0, details[1].strip())
                encrypted_password = details[2].strip()
                decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()
                self.password_entry.insert(0, decrypted_password)


    """===========================================Methods for opening tab/windows from main==========================================="""

    # Function to open File Transfer Window 
    def open_file_transfer_window(self):
        if not self.transport or not self.transport.is_active():
            messagebox.showerror("Error", "Not connected to Raspberry Pi.")
            return
        FileTransferWindow(self.transport)

    # Function to Open Instruction Manual
    def open_doc(self, event = None):
        doc_path = os.path.join(os.path.dirname(__file__), "doc/instruction_manual.txt")
        print(doc_path)
        webbrowser.open(doc_path)

    # Function to open Azure Configuration Window
    def open_mqtt_config_window(self):
        MQTTDetailsWindow(self.transport)
    
    # Function to open VPN Window 
    def open_vpn_window(self):
        OpenVpnWindow(self.transport)

    # Function to open Package Installer Window
    def open_package_installer_window(self):
        RaspbianPackages(self.transport)

    # Function to open About Window
    def open_about_window(self):
        AboutWindow()

    # Function to open Help Window
    def open_help_window(self):
        HelpWindow()

    # Function to open System Settings Window
    def open_system_settings(self):
        SystemSettings(self.transport)

    # Function to open System Services Window
    def open_service_settings(self):
        SystemServices(self.transport)

    # Function to Open Data Viewer Window
    def open_data_window(self):
        DataView(self.transport)

    # Function to Open Modbus Controller Platform
    def open_modbus_controller(self):
        MainController(self.transport)