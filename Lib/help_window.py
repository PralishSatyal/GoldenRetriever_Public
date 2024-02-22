# Import Relevant Libraies here
import tkinter as tk
import webbrowser
import os

"""Class to show contact information in the event the user needs help"""
class HelpWindow(tk.Toplevel):

    def __init__(self):
        super().__init__()
        self.transient()
        self.lift()

        self.title("Help")
        self.geometry("640x480")
        
        info_text = tk.Text(self, wrap=tk.WORD, height=10, width=60)
        info_text.pack(pady=10)
        
        # Insert text
        info_text.insert(tk.END, "To use this software, run through the instruction manual as outlined here ")
        info_text.insert(tk.END, "instruction_manual.csv", "link")
        info_text.insert(tk.END, "\n\nFor further enquiries please contact Pralish via:\npralishbusiness@gmail.com\nwww.pralish.com\n\n")
        
        # Configure the "link" tag to make it look like a hyperlink
        info_text.tag_configure("link", foreground="blue", underline=True)
        info_text.tag_bind("link", "<Button-1>", self.open_csv)
        info_text.config(state=tk.DISABLED)

    def open_csv(self, event = None):
        csv_path = os.path.join(os.path.dirname(__file__), "doc/instruction_manual.csv")
        print(csv_path)
        webbrowser.open(csv_path)

