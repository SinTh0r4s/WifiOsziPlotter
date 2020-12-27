# Enable recursive typing for python 3.7+ (from 3.10 it is build-in)
from __future__ import annotations

from osziplotter.modelcontroller.PlotInfo import PlotInfo

from typing import Dict, Type, List


class PlotEvents:

    _listeners: List[Type[PlotEvents]] = []
    _plots: Dict[int, Dict[float, PlotInfo]] = {}
    _selected_board: int = -1

    def __init__(self):
        self._listenerId = len(PlotEvents._listeners)
        PlotEvents._listeners.append(self)

    @classmethod
    def put(cls, plot: PlotInfo) -> None:
        if plot.board_uid not in PlotEvents._plots:
            PlotEvents._plots[plot.board_uid] = {}
        PlotEvents._plots[plot.board_uid][plot.timestamp] = plot
        if PlotEvents._selected_board == plot.board_uid:
            PlotEvents._update_listeners(PlotEvents._plots[PlotEvents._selected_board], plot)

    @classmethod
    def _update_listeners(cls, plots: Dict[float, PlotInfo], new_plot: PlotInfo = None) -> None:
        for listener in PlotEvents._listeners:
            listener.update_plot(plots, new_plot)

    @classmethod
    def _update_selected_board(cls, selected_board: int) -> None:
        PlotEvents._selected_board = selected_board
        PlotEvents.update_plot(PlotEvents._plots[selected_board])

    # Overwrite this method if you want to react on it
    def update_plot(self, plots: Dict[float, PlotInfo], new_plot: PlotInfo = None) -> None:
        pass
