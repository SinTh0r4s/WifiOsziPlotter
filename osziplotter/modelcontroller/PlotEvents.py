# Enable recursive typing for python 3.7+ (from 3.10 it is build-in)
from __future__ import annotations

from osziplotter.modelcontroller.PlotInfo import PlotInfo

from typing import Dict, Type, List, Tuple, ClassVar


class PlotEvents:

    _listeners: ClassVar[List[Type[PlotEvents]]] = []
    _plots: ClassVar[Dict[int, Dict[float, PlotInfo]]] = {}
    _selected_plot: ClassVar[Tuple[int, float]] = (-1, 0.0)

    def __init__(self, *args, **kwargs) -> None:
        PlotEvents._listeners.append(self)

    @classmethod
    def put(cls, plot: PlotInfo) -> None:
        if plot.board_uid not in PlotEvents._plots:
            PlotEvents._plots[plot.board_uid] = {}
        PlotEvents._plots[plot.board_uid][plot.timestamp] = plot
        PlotEvents._selected_plot = (plot.board_uid, plot.timestamp)
        PlotEvents._update_listeners(plot)

    @classmethod
    def _update_listeners(cls, visible_plot: PlotInfo = None) -> None:
        uid, _ = PlotEvents._selected_plot
        for listener in PlotEvents._listeners:
            listener.update_plot(PlotEvents._plots[uid], visible_plot)

    @classmethod
    def _update_selected_board(cls, uid: int) -> None:
        if uid in PlotEvents._plots and len(PlotEvents._plots[uid]) > 0:
            plot = PlotEvents._plots[uid][-1]
            PlotEvents._selected_plot = (uid, plot.timestamp)
            PlotEvents._update_listeners(plot)
        else:
            PlotEvents._update_listeners(None)

    @classmethod
    def update_selected_plot(cls, timestamp: float) -> None:
        uid, _ = PlotEvents._selected_plot
        PlotEvents._selected_plot = (uid, timestamp)
        PlotEvents._update_listeners(PlotEvents._plots[uid][timestamp])

    @classmethod
    def update_plot_domain(cls, domain: str):
        uid, timestamp = PlotEvents._selected_plot
        PlotEvents._plots[uid][timestamp].domain = domain
        PlotEvents.update_selected_plot(timestamp)

    # Overwrite this method if you want to react on it
    def update_plot(self, plots: Dict[float, PlotInfo], visible_plot: PlotInfo = None) -> None:
        pass
