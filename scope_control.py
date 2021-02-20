"""Widgets for doing direct control of the scopes"""

from qtpy import QtWidgets, QtCore

class OutputChannelWidget(QtWidgets.QWidget):
    """Individual Channel Control"""

    # TODO pull validation data from the PSU implementation
    # TODO pull channel on/off states

    def __init__(self, parent, device, channel: int):
        super().__init__(parent)

        self.device = device
        self.channel = channel

        # Read current/voltage, enabled
        voltage = self.device.get_channel_voltage(self.channel)
        current = self.device.get_channel_current(self.channel)

        self.setLayout(QtWidgets.QGridLayout(self))

        self.label = QtWidgets.QLabel(f"Channel {self.channel + 1}")
        self.layout().addWidget(self.label, 0, 0)
        self.enable_button = QtWidgets.QCheckBox("Enabled", )
        self.enable_button.clicked.connect(self.enable_channel)
        self.layout().addWidget(self.enable_button, 0, 1, 1, 3)
        self.layout().setAlignment(self.enable_button, QtCore.Qt.AlignRight)

        self.voltage_label = QtWidgets.QLabel("Voltage")
        self.layout().addWidget(self.voltage_label, 1, 0)
        self.voltage_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.voltage_slider.setMinimum(0)
        self.voltage_slider.setMaximum(32)
        self.voltage_slider.setMinimumWidth(300)
        self.voltage_slider.sliderMoved.connect(self.update_voltage_From_slider)
        self.voltage_slider.setValue(int(voltage))
        self.layout().addWidget(self.voltage_slider, 1, 1)
        self.voltage_value = QtWidgets.QDoubleSpinBox(self)
        self.voltage_value.setMinimum(0.00)
        self.voltage_value.setMaximum(32.00)
        self.voltage_value.editingFinished.connect(self.set_voltage)
        self.voltage_value.setValue(voltage)
        self.layout().addWidget(self.voltage_value, 1, 2)
        self.voltage_set = QtWidgets.QPushButton("Set Value")
        self.voltage_set.clicked.connect(self.set_voltage)
        self.layout().addWidget(self.voltage_set, 1, 3)

        self.current_label = QtWidgets.QLabel("Current")
        self.layout().addWidget(self.current_label, 2, 0)
        self.current_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.current_slider.setMinimum(0)
        self.current_slider.setMaximum(32)
        self.current_slider.setMinimumWidth(300)
        self.current_slider.sliderMoved.connect(self.update_current_from_slider)
        self.current_slider.setValue(int(current * 10))
        self.layout().addWidget(self.current_slider, 2, 1)
        self.current_value = QtWidgets.QDoubleSpinBox(self)
        self.current_value.setMinimum(0.00)
        self.current_value.setMaximum(3.20)
        self.current_value.editingFinished.connect(self.set_current)
        self.current_value.setValue(current)
        self.layout().addWidget(self.current_value, 2, 2)
        self.current_set = QtWidgets.QPushButton("Set Value")
        self.current_set.clicked.connect(self.set_current)
        self.layout().addWidget(self.current_set, 2, 3)

    def set_voltage(self):
        self.device.set_channel_voltage(self.channel, self.voltage_value.value())

    def set_current(self):
        self.device.set_channel_current(self.channel, self.current_value.value())

    def update_voltage_From_slider(self, slider_voltage: int):
        self.voltage_value.setValue(float(slider_voltage))

    def update_current_from_slider(self, slider_current: int):
        self.current_value.setValue(float(slider_current / 10))

    def enable_channel(self, checked: bool):
        self.device.enable_channel(self.channel, checked)

    def refresh_voltage(self, voltage: float):
        """Slot to refresh displayed voltage values"""
        raise NotImplementedError

    def refresh_current(self, current: float):
        """Slot to refresh displayed current values"""
        raise NotImplementedError


class ControlWidget(QtWidgets.QWidget):
    """Generic Control Widget that supports N channels"""

    def __init__(self, parent):
        super().__init__(parent)

        self.device = None
        self.channels = []

        self.setLayout(QtWidgets.QVBoxLayout(self))

    # TODO should accept ABC for a PSU, too lazy to do now
    def open_device(self, device):
        self.device = device

        # Clear out all widgets, how do I delete again? widget.deleteLater()
        for channel in self.channels:
            self.layout().removeWidget(channel)
            channel.deleteLater()
        self.channels = []

        # Add our widgets back
        for i in range(device.num_channels):
            self.channels.append(OutputChannelWidget(self, self.device, i))
            self.layout().addWidget(self.channels[-1])

