"""
    (C) Pralish Satyal 2023

    A program to allow flashing metering software onto 
    a Raspberry Pi with Control 
    into what modbus map the Pi
    can use.

    pralishbusiness@gmail.com
    www.pralish.com
"""

# Import Libraries here
import tkinter as tk
from Lib.main_app import MainApp

        
if __name__ == "__main__":
    print("Starting the application now")
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
