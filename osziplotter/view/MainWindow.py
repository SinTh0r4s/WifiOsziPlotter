from osziplotter.modelcontroller.BoardEvents import BoardEvents
from osziplotter.network.Network import Network
from osziplotter.view.BoardComboBox import BoardComboBox
from osziplotter.view.BoardInfoLabel import BoardInfoLabel
from osziplotter.view.ExportWidget import ExportWidget
from osziplotter.view.PlotComboBox import PlotComboBox
from osziplotter.view.PlotWidget import PlotWidget
from osziplotter.view.TriggerCommandWidget import TriggerCommandWidget

from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QFrame, QSpacerItem, QSizePolicy,\
    QPushButton, QApplication
from PyQt5.QtCore import QTimer


class MainWindow(QMainWindow):
    def __init__(self, network: Network, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self._network = network
        self.setWindowTitle("WiFi Oszi by Johann Bernhardt")
        self.setGeometry(100, 100, 1000, 600)

        self._widget = QWidget()
        self._layout = QHBoxLayout()
        self._layout.setSpacing(10)

        self._board_widget = QWidget()
        self._board_layout = QVBoxLayout()
        self._board_combo_box = BoardComboBox()
        self._board_layout.addWidget(self._board_combo_box)
        self._board_layout.addItem(QSpacerItem(0, 30, QSizePolicy.Expanding, QSizePolicy.Fixed))
        self._board_info_label = BoardInfoLabel()
        self._board_layout.addWidget(self._board_info_label)
        self._board_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))
        self._board_trigger_command_widget = TriggerCommandWidget(self._network)
        self._board_layout.addWidget(self._board_trigger_command_widget)
        self._board_widget.setLayout(self._board_layout)
        self._layout.addWidget(self._board_widget)

        self._layout.addWidget(VLine())

        self._plot_widget = QWidget()
        self._plot_layout = QVBoxLayout()
        self._plot_toolbar_layout = QHBoxLayout()
        self._plot_toolbar_plot_combo_box = PlotComboBox()
        self._plot_toolbar_layout.addWidget(self._plot_toolbar_plot_combo_box)
        self._plot_toolbar_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))
        self._plot_toolbar_export_widget = ExportWidget()
        self._plot_toolbar_layout.addWidget(self._plot_toolbar_export_widget)
        self._plot_toolbar_about_button = QPushButton(self)
        self._plot_toolbar_about_button.clicked.connect(QApplication.aboutQt)
        self._plot_toolbar_about_button.setText("About Qt")
        self._plot_toolbar_layout.addWidget(self._plot_toolbar_about_button)
        self._plot_layout.addLayout(self._plot_toolbar_layout)
        self._plot_plot_widget = PlotWidget()
        self._plot_layout.addWidget(self._plot_plot_widget)
        self._plot_widget.setLayout(self._plot_layout)
        self._layout.addWidget(self._plot_widget)

        self._widget.setLayout(self._layout)
        self.setCentralWidget(self._widget)

        self._timer = QTimer()
        self._timer.timeout.connect(self._tick)
        self._timer.start(50)

    def _tick(self) -> None:
        self._network.handle_events()
        BoardEvents.tick()


class HLine(QFrame):

    def __init__(self, *args, **kwargs) -> None:
        super(HLine, self).__init__(*args, **kwargs)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class VLine(QFrame):

    def __init__(self, *args, **kwargs) -> None:
        super(VLine, self).__init__(*args, **kwargs)
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)
