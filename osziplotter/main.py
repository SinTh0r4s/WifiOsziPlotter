from osziplotter.network.Network import Network
from osziplotter.view.MainWindow import MainWindow

from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
network = Network()
network.listen()
main_window = MainWindow(network)
main_window.show()
sys.exit(app.exec_())
