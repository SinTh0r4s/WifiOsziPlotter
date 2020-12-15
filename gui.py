# lib imports
from tkinter import Tk, LEFT, RIGHT, Y
import numpy as np

# local import
from BoardInfoDisplay import BoardInfoDisplay
from SamplePlotter import SamplePlotter

master = Tk()
master.wm_title("Wifi Oszi")

b = BoardInfoDisplay(master=master)
b.pack(side=LEFT)

s = SamplePlotter(master=master)
s.pack(side=LEFT)

s.refresh(np.zeros(100))

master.mainloop()
