#!/usr/bin/env python3

from helpers import usbtmc_backend
from qtpy import QtWidgets, QtCore
import sys

from siglent import SPD3303
from scope_control import ControlWidget

class ScopeSelectorWidget(QtWidgets.QWidget):
    """Small widget to select the proper scope device"""

    select = QtCore.Signal(str)

    # TODO refresh
    # TODO pull in more than just device name
    def __init__(self, parent):
        super().__init__(parent)

        self.setLayout(QtWidgets.QHBoxLayout(self))

        self.devices = QtWidgets.QComboBox(self)
        self.devices.addItems(usbtmc_backend().getDeviceList())
        self.layout().addWidget(self.devices)
        self.button = QtWidgets.QPushButton("Select Device")
        self.button.clicked.connect(self._select_device)
        self.layout().addWidget(self.button)

    def _select_device(self):
        if self.devices.currentText():
            self.select.emit(self.devices.currentText())

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PSU Control GUI")

        self.setCentralWidget(QtWidgets.QWidget())
        self.central_layout = QtWidgets.QVBoxLayout(self.centralWidget())

        self.device_selector = ScopeSelectorWidget(self)
        self.device_selector.select.connect(self.open_device)
        self.central_layout.addWidget(self.device_selector)

        self.control = ControlWidget(self)
        self.central_layout.addWidget(self.control)

    def open_device(self, device: str):
        device = SPD3303(device)
        self.control.open_device(device)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()

    sys.exit(app.exec_())
