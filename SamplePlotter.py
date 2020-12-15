# lib imports
from tkinter import Frame, TOP, BOTH
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
import numpy as np


class SamplePlotter(Frame):

    def __init__(self, master):
        Frame.__init__(self, master=master)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH)
        self.toolbar = NavigationToolbar2Tk(self.canvas, master)

        def on_key_press(event):
            key_press_handler(event, self.canvas, self.toolbar)
        self.canvas.mpl_connect("key_press_event", on_key_press)

    def refresh(self, data:np.array):
        self.figure.add_subplot(111).plot(data)
        self.canvas.draw()
        self.toolbar.update()
