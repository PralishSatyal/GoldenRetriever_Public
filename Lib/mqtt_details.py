import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, font
import paramiko
from Lib.utils import read_file
import json

class MQTTDetailsWindow(tk.Toplevel):

    def __init__(self, transport):
        super().__init__()
        self.transient()
        self.lift()

        self.title("MQTT Details")
        self.geometry("720x540")
        self.transport = transport
        
        self.connected_username = read_file("login.txt")

        self.json_file_path = None
        self.cert_file_path = None
        self.mqtt_remote_dir = f"/home/{self.connected_username}/PiMeter/Lib/Azure_Connection/"

        self.header_font = font.Font(size=16, weight="bold")
        self.label_font = font.Font(size=12)
        self.info_font = font.Font(size=10)

        self.create_widgets()

    def create_widgets(self):

        # Create the notebook (tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

        # Create frames for each tab
        self.home_mqtt_frame = tk.Frame(self.notebook)
        self.azure_mqtt_frame = tk.Frame(self.notebook)
        self.thingsboard_mqtt_frame = tk.Frame(self.notebook)

        # Add frames to the notebook
        self.notebook.add(self.home_mqtt_frame, text = "Home")
        self.notebook.add(self.azure_mqtt_frame, text="Azure MQTT")
        self.notebook.add(self.thingsboard_mqtt_frame, text="Thingsboard MQTT")

        """Home MQTT Details Options and Backend"""
        tk.Label(self.home_mqtt_frame, text="MQTT Options Selector", font=self.header_font).grid(row=0, column=0, columnspan=2, pady=(20, 10))
        tk.Label(self.home_mqtt_frame, text="This window shows you options for creating a new MQTT configuration.", font=self.label_font).grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")
        tk.Label(self.home_mqtt_frame, text="If you are sending data to Azure IoTHUB, please navigate to the Azure MQTT window.", font=self.info_font).grid(row=3, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")
        tk.Label(self.home_mqtt_frame, text="If you are sending data to Thingsboard, please navigate to the respective tab.", font=self.info_font).grid(row=4, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")


        """Azure MQTT Details Options and Backend """
        # Azure MQTT Tab Details
        tk.Label(self.azure_mqtt_frame, text="Azure Connection Configuration", font=self.header_font).grid(row=0, column=0, columnspan=2, pady=(20, 10))
        tk.Label(self.azure_mqtt_frame, text="Select your connection details JSON file and your Azure Certifacte file.", font=self.label_font).grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")
        tk.Label(self.azure_mqtt_frame, text="The connection_details.json file should be saved as so and is obtained from the Azure Iot Portal.", font=self.info_font).grid(row=3, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")
        tk.Label(self.azure_mqtt_frame, text="The Azure Certifcate is a .pem file obtained from Internal team and/or on Azure.", font=self.info_font).grid(row=4, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")

        # Buttons (back-end) for Azure Window
        self.json_select_button = tk.Button(self.azure_mqtt_frame, text="Select Connection json", command=lambda: self.select_file("json"))
        self.json_select_button.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.cert_select_button = tk.Button(self.azure_mqtt_frame, text="Select Azure Certifcate", command=lambda: self.select_file("cert"))
        self.cert_select_button.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        self.send_button = tk.Button(self.azure_mqtt_frame, text="Send both files", state=tk.DISABLED, command=self.send_file_azure)
        self.send_button.grid(row=6, column=1, padx=10, pady=10, sticky="e")


        """Thingsboard MQTT Details Options and Backend"""

        # Things Board MQTT Tab Details
        tk.Label(self.thingsboard_mqtt_frame, text="Things Board Configuration", font=self.header_font).grid(row=0, column=0, columnspan=2, pady=(20, 10))
        tk.Label(self.thingsboard_mqtt_frame, text="Please enter the relevant details for your thingsboard connection", font=self.label_font).grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")
        tk.Label(self.thingsboard_mqtt_frame, text="You will need to enter the MQTT topic, username, password and broker", font=self.info_font).grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")
        tk.Label(self.thingsboard_mqtt_frame, text="Then, press the send button and a configuration will be sent to the Pi.", font=self.info_font).grid(row=3, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")


        # Text entry widgets for Thingsboard Window
        self.broker_label = tk.Label(self.thingsboard_mqtt_frame, text="broker:")
        self.broker_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.broker_entry = tk.Entry(self.thingsboard_mqtt_frame)
        self.broker_entry.grid(row=4, column=1, padx=10, pady=10)

        self.port_label = tk.Label(self.thingsboard_mqtt_frame, text="port:")
        self.port_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.port_entry = tk.Entry(self.thingsboard_mqtt_frame)
        self.port_entry.grid(row=5, column=1, padx=10, pady=10)

        # Text entry widgets for Thingsboard Window
        self.topic_label = tk.Label(self.thingsboard_mqtt_frame, text="topic:")
        self.topic_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.topic_entry = tk.Entry(self.thingsboard_mqtt_frame)
        self.topic_entry.grid(row=6, column=1, padx=10, pady=10)

        self.clientid_label = tk.Label(self.thingsboard_mqtt_frame, text="client id:")
        self.clientid_label.grid(row=7, column=0, padx=10, pady=10, sticky="w")
        self.clientid_entry = tk.Entry(self.thingsboard_mqtt_frame)
        self.clientid_entry.grid(row=7, column=1, padx=10, pady=10)

        # Text entry widgets for Thingsboard Window
        self.username_label = tk.Label(self.thingsboard_mqtt_frame, text="username:")
        self.username_label.grid(row=8, column=0, padx=10, pady=10, sticky="w")
        self.username_entry = tk.Entry(self.thingsboard_mqtt_frame)
        self.username_entry.grid(row=8, column=1, padx=10, pady=10)

        # Text entry widgets for Thingsboard Window
        self.password_label = tk.Label(self.thingsboard_mqtt_frame, text="password:")
        self.password_label.grid(row=9, column=0, padx=10, pady=10, sticky="w")
        self.password_entry = tk.Entry(self.thingsboard_mqtt_frame, show = "*")
        self.password_entry.grid(row=9, column=1, padx=10, pady=10)

        # After creating the connection file
        self.send_button = tk.Button(self.thingsboard_mqtt_frame, text="Send thingsboard data", state=tk.ACTIVE, command=self.send_thingsboard_data)
        self.send_button.grid(row=10, column=1, padx=10, pady=10, sticky="e")


    def create_connection_file(self):
        broker = self.broker_entry.get().strip()
        port = self.port_entry.get().strip()
        topic = self.topic_entry.get().strip()
        client_id = self.clientid_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Thingsboard MQTT Tab
        things_data = {
            "time_series_conn_info": {
                "host": broker,
                "port": port,
                "topic": topic,
                "client_id":client_id,
                "username": username,
                "password": password
            }
        }

        file_path = 'Lib/connection_details.json'
        with open(file_path, 'w') as file:
            print("Creating JSON file for thingsboard data")
            json.dump(things_data, file, indent =3)
            
        return file_path


    def send_thingsboard_data(self):
        # Firstly, let's create the connection file and get its path
        local_file_path = self.create_connection_file()

        if not self.transport or not self.transport.is_active():
            messagebox.showerror("Error", "Not connected to Raspberry Pi.")
            return
        
        if not local_file_path:  # Check if the local file path is set
            messagebox.showerror("Error", "Error creating Thingsboard configuration file.")
            return

        remote_filename = local_file_path.split("/")[-1]
        remote_path = self.mqtt_remote_dir + remote_filename

        try:
            sftp = paramiko.SFTPClient.from_transport(self.transport)
            sftp.put(local_file_path, remote_path)
            sftp.close()

            messagebox.showinfo("Success", f"File '{local_file_path}' sent successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Function to select file if you are in the Azure Window
    def select_file(self, file_type):
        file_path = filedialog.askopenfilename()

        if file_path:
            if file_type == "json":
                self.json_file_path = file_path
            elif file_type == "cert":
                self.cert_file_path = file_path

            if hasattr(self, "json_file_path") and hasattr(self, "cert_file_path"):
                self.send_button.config(state=tk.NORMAL)

    # Function to send file for connection details
    def send_file(self, local_file_path, remote_dir):
        if not self.transport or not self.transport.is_active():
            messagebox.showerror("Error", "Not connected to Raspberry Pi.")
            return

        try:
            sftp = paramiko.SFTPClient.from_transport(self.transport)

            remote_filename = local_file_path.split("/")[-1]
            remote_path = remote_dir + remote_filename

            sftp.put(local_file_path, remote_path)
            sftp.close()

            messagebox.showinfo("Success", f"File '{local_file_path}' sent successfully.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Function to send azure connection details
    def send_file_azure(self):
        if not self.json_file_path or not self.cert_file_path:
            messagebox.showerror("Error", "Both files need to be selected before sending.")
            return
        
        # Send the relevent azure files
        self.send_file(self.json_file_path, self.mqtt_remote_dir)
        self.send_file(self.cert_file_path, self.mqtt_remote_dir)
