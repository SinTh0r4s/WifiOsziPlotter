# lib imports
from tkinter import Tk, LEFT, RIGHT, Y
import numpy as np

# local import
from BoardInfoDisplay import BoardInfoDisplay
from SamplePlotter import SamplePlotter
from BoardInfo import BoardInfo
from Network import Network


def gui():
    master = Tk()
    master.wm_title("Wifi Oszi")

    info = BoardInfo()
    info.v_ref = 3300
    info.sample_time = 1000
    info.sample_time_unit = "μs"
    info.frequency = 500
    info.frequency_unit = "kHz"
    info.resolution = 8
    info.samples = 500
    info.model = "TestBoard"
    info.adc = "Imaginary"

    b = BoardInfoDisplay(master=master)
    b.pack(side=LEFT)
    b.refresh(info)

    s = SamplePlotter(master=master)
    s.pack(side=LEFT)
    s.refresh(info, np.arange(0, 3300, 3300 / info.samples))
    s.reset()

    def draw(data):
        print("draw")
        print(data)
        print(len(data[0]))

    def update_boards():
        print("update boards")

    network = Network(draw, update_boards)
    master.after(100, network.handle_events)

    master.mainloop()


if __name__ == '__main__':
    gui()