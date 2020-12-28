from osziplotter.network.Network import Network
from osziplotter.view.MainWindow import MainWindow

import sys
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    network = Network()
    network.listen()
    m = MainWindow(network)
    m.show()
    sys.exit(app.exec_())
