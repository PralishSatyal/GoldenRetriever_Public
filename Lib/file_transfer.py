# Import Relevant Libraries here
import tkinter as tk
from tkinter import filedialog, messagebox, font
import paramiko
from Lib.utils import read_file

"""Class for flashing PiMeter Zip file to Device"""
class FileTransferWindow(tk.Toplevel):
    def __init__(self, transport):
        super().__init__()
        self.transient()  # make window transient to its master
        # self.grab_set()   # grab the focus
        self.lift()       # bring the window to the front

        self.title("File Transfer App")
        self.geometry("640x480")
        
        self.transport = transport
        self.connected_username = read_file("login.txt")[0]
        self.file_path = None
        
        # Define some font styles
        self.header_font = font.Font(size=16, weight="bold")
        self.label_font = font.Font(size=12)
        self.info_font = font.Font(size=10)
        self.create_widgets()

    # Function to create widgets and buttons
    def create_widgets(self):
        self.select_button = tk.Button(self, text="Select PiMeter Zip", command=self.select_file)
        self.select_button.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.send_button = tk.Button(self, text="Send File", state=tk.DISABLED, command=self.send_file)
        self.send_button.grid(row=5, column=1, padx=10, pady=10, sticky="e")

        self.loaded_file_label = tk.Label(self, text="Loaded File:")
        self.loaded_file_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")

        self.loaded_file_entry = tk.Entry(self, state=tk.DISABLED)
        self.loaded_file_entry.grid(row=7, column=0, padx=10, pady=10, sticky="we")

        # Main header
        self.header_label = tk.Label(self, text="PiMeter Software File Extractor", font=self.header_font)
        self.header_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        # Instruction label
        self.instruction_label1 = tk.Label(self, text="Select the PiMeter Zip file to send to the device\n", font=self.label_font)
        self.instruction_label1.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")

        # Text Information Label
        self.information_label1 = tk.Label(self, text = "The Zip File is found on the NASBOX and can be requested internally.", font = self.info_font)
        self.information_label1.grid(row = 3, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")

        self.information_label2 = tk.Label(self, text = "Once loaded, the zip file will be extracted into the relevant workspace on the device", font = self.info_font)
        self.information_label2.grid(row = 4, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")

        # Spacer between buttons
        self.spacer_label = tk.Label(self, height=2)  # Empty label to give some space between widgets
        self.spacer_label.grid(row=5, column=0, columnspan=2)

    # Function to select relevant file
    def select_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.loaded_file_entry.config(state=tk.NORMAL)
            self.loaded_file_entry.delete(0, tk.END)
            self.loaded_file_entry.insert(0, self.file_path)
            self.loaded_file_entry.config(state=tk.DISABLED)
            self.send_button.config(state=tk.NORMAL)

    # Function to send file and unzip using specific directory
    def send_file(self):
        if not self.transport or not self.transport.is_active():
            messagebox.showerror("Error", "Not connected to Raspberry Pi.")
            return
        
        try:
            sftp = paramiko.SFTPClient.from_transport(self.transport)  # This is the correct way to initiate SFTP
            
            remote_dir = f"/home/{self.connected_username}/"  
            remote_path = remote_dir + self.file_path.split("/")[-1]
            sftp.put(self.file_path, remote_path)
            
            # If the file is a zip file, unzip it remotely
            if self.file_path.endswith('.zip'):
                ssh = self.transport.open_session()
                ssh.exec_command(f'unzip {remote_path} -d {remote_dir}')
                while not ssh.exit_status_ready():
                    # Wait for files to be unzipped before closing ssh
                    pass
                ssh.close()


            sftp.close()
            messagebox.showinfo("Success", "File sent successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
