# lib imports
from tkinter import Frame, Label, StringVar, LEFT, BOTH, TOP, X, W

# local imports
from osziplotter.modelcontroller.BoardInfo import BoardInfo
from Util import to_one_decimal


class BoardInfoDisplay(Frame):

    def __init__(self, master):
        Frame.__init__(self, master, width=200, height=300)
        self.pack_propagate(0)

        self.board_var = StringVar()
        self.board = StringEntry(master=self, label="Board:", string_ref=self.board_var)
        self.board.pack(side=TOP, fill=X)

        self.adc_var = StringVar()
        self.adc = StringEntry(master=self, label="ADC:", string_ref=self.adc_var)
        self.adc.pack(side=TOP, fill=X)

        self.resolution_var = StringVar()
        self.resolution = StringEntry(master=self, label="Resolution:", string_ref=self.resolution_var)
        self.resolution.pack(side=TOP, fill=X)

        self.frequency_var = StringVar()
        self.frequency = StringEntry(master=self, label="Frequency:", string_ref=self.frequency_var)
        self.frequency.pack(side=TOP, fill=X)

        self.samples_var = StringVar()
        self.samples = StringEntry(master=self, label="Samples:", string_ref=self.samples_var)
        self.samples.pack(side=TOP, fill=X)

        self.sample_time_var = StringVar()
        self.sample_time = StringEntry(master=self, label="Sample time:", string_ref=self.sample_time_var)
        self.sample_time.pack(side=TOP, fill=X)

        self.v_ref_var = StringVar()
        self.v_ref = StringEntry(master=self, label="Vref:", string_ref=self.v_ref_var)
        self.v_ref.pack(side=TOP, fill=X)

        # init with defaults
        info = BoardInfo()
        self.refresh(info)

    def refresh(self, info: BoardInfo) -> None:
        self.board_var.set(info.model)
        self.adc_var.set(info.adc)
        self.resolution_var.set(str(info.resolution) + " bits")
        self.frequency_var.set(to_one_decimal(info.frequency) + " " + info.frequency_unit)
        self.samples_var.set(info.num_samples)
        self.sample_time_var.set(to_one_decimal(info.sample_time) + " " + info.sample_time_unit)
        self.v_ref_var.set(str(info.v_ref) + " mV")


class StringEntry(Frame):

    def __init__(self, master, label: str, string_ref: StringVar):
        Frame.__init__(self, master)
        self.static = Frame(master=self, width=100)
        self.static.pack_propagate(0)
        self.static_label = Label(master=self.static, text=label, anchor=W)
        self.static_label.pack(side=LEFT, fill=BOTH)
        self.static.pack(side=LEFT, fill=BOTH)
        self.label = Label(master=self, textvariable=string_ref, anchor=W)
        self.label.pack(side=LEFT, fill=BOTH)
