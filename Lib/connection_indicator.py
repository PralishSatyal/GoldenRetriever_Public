# Import Relevent Libraries
import tkinter as tk

"""Class for showing SSH connection status with the device, via an LED"""
class ConnectionIndicator(tk.Canvas):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.draw_circle("lightgrey")

    # Function to draw circle geometry 
    def draw_circle(self, color):
        self.delete("all")
        x0, y0, x1, y1 = 0, 0, 20, 20
        self.create_oval(x0, y0, x1, y1, fill=color, outline="")
