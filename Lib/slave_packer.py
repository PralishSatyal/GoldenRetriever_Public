# Import Relevant Libraries
import tkinter as tk
from tkinter import ttk

# Import modbus maps module for class inheritance of window
from Lib.modbus_maps import ModbusMap

"""Class to handle logic for Slaves and display modbus settings data per slave"""


class SlavePacker(ModbusMap):

    # Initialisation 
    def __init__(self, transport):
        super().__init__(transport)

        self.title("Slave Packer")
        self.geometry('840x630')
        
        self.create_slave_widgets()
        
    # Method to create our slave specific widgets (the +slave)
    def create_slave_widgets(self):
        self.note = ttk.Notebook(self)
        self.slaves = []
        self.add_slave_frame = ttk.Frame(self.note)
        self.note.add(self.add_slave_frame, text='+')
        self.note.bind("<<NotebookTabChanged>>", self.on_slave_selected)
        self.note.grid(row=0, column = 0, padx=5, pady=5)

    # If the + slave is selected, create a new slave
    def on_slave_selected(self, event):
        if self.note.index(tk.CURRENT) == self.note.index(self.add_slave_frame):
            self.add_slave()

    # Function to close the slave
    def close_slave(self, slave):
        self.note.forget(slave['frame'])
        self.slaves.remove(slave)

    # Update the slave name 
    def update_slave_name(self, event, slave, entry):
        new_name = entry.get()
        if new_name.isdigit():
            self.note.tab(slave, text=f"slave {new_name}")


    """Need to change so that when we add a slave, we create a separate modbus map entry area"""
    def add_slave(self):
        # Create the slave_frame as a part of the notebook.
        slave_frame = ttk.Frame(self.note)
        
        # Instead of setting attributes on slave_frame directly, we'll store its related data in a dictionary.
        slave = {"frame": slave_frame, "file_path": None}

        # Initialize widgets for each slave.
        slave['csv_display'] = self.initialise_widgets(slave_frame, slave)

        # Create a style for the slaves
        style = ttk.Style()
        style.configure('TNotebook.slave', padding=[10, 10])

        slave_label = f"Slave {len(self.slaves) + 1}"  # We add 1 because the current slave hasn't been added yet.
        
        # Add the slave to the notebook.
        self.note.insert(self.note.index(self.add_slave_frame), slave_frame, text=slave_label)

        # Add a label for slave ID input
        slave_id_label = ttk.Label(slave_frame, text="slave_id:")
        slave_id_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")  # position the label at row=0, column=0

        # Add Entry widget for slave ID input
        slave_id_entry = ttk.Entry(slave_frame)
        slave_id_entry.bind('<Return>', lambda e, s=slave: self.update_slave_name(e, s['frame'], slave_id_entry))
        slave_id_entry.grid(row=0, column=2, padx=5, pady=5, sticky='w')

        # Add the slave_id_entry to the slave dictionary
        slave['slave_id_entry'] = slave_id_entry

        if self.mode == 'TCP':
            # Entry Point for IP Address as we want this per each slave
            ip_address_label = ttk.Label(slave_frame, text="Device IP Address:")
            ip_address_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
            ip_address_entry = ttk.Entry(slave_frame)
            ip_address_entry.grid(row=2, column=2, padx=5, pady=5, sticky='w')
            slave['ip_address_entry'] = ip_address_entry
        
        elif self.mode == 'RTU':
            self.port_label = tk.Label(self, text = "Port:")
            self.port_label.grid(row = 5, column = 0, padx=5, pady=5, sticky="w")
            
            port_options = ['/dev/ttyUSB0', '/dev/ttyACM0']
            self.port_combobox = ttk.Combobox(self, values=port_options)
            self.port_combobox.grid(row=6, column=0, padx=5, pady=5, sticky="w")
            self.port_combobox.set(port_options[0])

            # Baud Rate Settings
            self.baud_label = tk.Label(self, text="Baud Rate:")
            self.baud_label.grid(row=9, column=0, padx=5, pady=5, sticky="w")

            baud_options = ['9600', '14400', '19200', '38400', '57600', '115200']
            self.baud_combobox = ttk.Combobox(self, values=baud_options)
            self.baud_combobox.grid(row=10, column=0, padx=5, pady=5, sticky="w")
            self.baud_combobox.set(baud_options[0])

            # Data bits settings
            self.bits_label = tk.Label(self, text="Data bits")
            self.bits_label.grid(row=11, column=0, padx=5, pady=5, sticky="w")

            bits_options = ['7',  '8']
            self.bits_combobox = ttk.Combobox(self, values=bits_options)
            self.bits_combobox.grid(row=12, column=0, padx=5, pady=5, sticky="w")
            self.bits_combobox.set(bits_options[1])

            # Parity bits settings
            self.parity_label = tk.Label(self, text="Parity")
            self.parity_label.grid(row=13, column=0, padx=5, pady=5, sticky="w")
            parity_options = ['None', 'Odd',  'Even'] 

            self.parity_combobox = ttk.Combobox(self, values=parity_options)
            self.parity_combobox.grid(row=14, column=0, padx=5, pady=5, sticky="w")
            self.parity_combobox.set(parity_options[0])

            # Stop bits settings
            self.stop_bits_label = tk.Label(self, text="Stop bits")
            self.stop_bits_label.grid(row=15, column=0, padx=5, pady=5, sticky="w")

            stop_bits_options = ['1', '2']
            self.stop_bits_combobox = ttk.Combobox(self, values=stop_bits_options)
            self.stop_bits_combobox.grid(row=16, column=0, padx=5, pady=5, sticky="w")
            self.stop_bits_combobox.set(stop_bits_options[0])

            # Time out settings
            self.time_out_label = tk.Label(self, text = 'Time Out')
            self.time_out_label.grid(row=17, column=0, padx=5, pady=5, sticky = "w")
            self.time_out_entry = tk.Entry(self)
            self.time_out_entry.grid(row=18, column=0, padx=5, pady=5, sticky = "w")

            slave['port_combobox'] = self.port_combobox
            slave['baud_combobox'] = self.baud_combobox
            slave['bits_combobox'] = self.bits_combobox
            slave['parity_combobox'] = self.parity_combobox
            slave['stop_bits_combobox'] = self.stop_bits_combobox
            slave['time_out_entry'] =  self.time_out_entry

        # Place the close button in the middle of the slave.
        close_button = ttk.Button(slave_frame, text="Remove slave", width=16, command=lambda s=slave: self.close_slave(s))
        close_button.grid(row=1, column=2, padx=5, pady=5, sticky='w')

        # Add the slave dictionary to the slaves list.
        self.slaves.append(slave)
        self.note.select(slave_frame)
