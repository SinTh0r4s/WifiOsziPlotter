# Enable recursive typing for python 3.7+ (from 3.10 it is build-in)
from __future__ import annotations

from typing import Dict, Type, List
from PlotInfo import PlotInfo


class PlotEvents:

    __listeners: List[Type[PlotEvents]] = []
    __plots: Dict[int, Dict[float, PlotInfo]] = {}
    __selected_board: int = -1

    def __init__(self):
        self.__listenerId = len(PlotEvents.__listeners)
        PlotEvents.__listeners.append(self)

    @classmethod
    def put(cls, plot: PlotInfo) -> None:
        if plot.board_uid not in PlotEvents.__plots:
            PlotEvents.__plots[plot.board_uid] = {}
        PlotEvents.__plots[plot.board_uid][plot.timestamp] = plot
        if PlotEvents.__selected_board == plot.board_uid:
            PlotEvents.__update_listeners(PlotEvents.__plots[PlotEvents.__selected_board], plot)

    @classmethod
    def __update_listeners(cls, plots: Dict[float, PlotInfo], new_plot: PlotInfo = None) -> None:
        for listener in PlotEvents.__listeners:
            listener.update_plot(plots, new_plot)

    @classmethod
    def __update_selected_board(cls, selected_board: int) -> None:
        PlotEvents.__selected_board = selected_board
        PlotEvents.update_plot(PlotEvents.__plots[selected_board])

    # Overwrite this method if you want to react on it
    def update_plot(self, plots: Dict[float, PlotInfo], new_plot: PlotInfo = None) -> None:
        pass
