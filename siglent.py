from helpers import usbtmc_backend
import universal_usbtmc as usbtmc

class SPD3303:
    """SPD3303-X/E"""

    # TODO ABC for a PSU
    # TODO how do I more properly manage the channel number...

    def __init__(self, device: str):
        self._device: usbtmc.Instrument = usbtmc_backend().Instrument(device)
        # HACK because siglent can't write firmware...
        self._device.SLEEPTIME_BEFORE_READ = 0.1

        self._ident = self._device.query("*IDN?")

    @property
    def num_channels(self) -> int:
        return 2

    def set_channel_voltage(self, channel: int, value: float):
        if channel < 0 or channel >= 2:
            raise Exception("Invalid channel!")

        self._device.write(f"CH{channel + 1}:VOLT {value}")

    def set_channel_current(self, channel: int, value: float):
        if channel < 0 or channel >= 2:
            raise Exception("Invalid channel!")

        self._device.write(f"CH{channel + 1}:CURR {value}")

    def get_channel_voltage(self, channel: int) -> float:
        if channel < 0 or channel >= 2:
            raise Exception("Invalid channel!")

        return float(self._device.query(f"CH{channel + 1}:VOLT?"))

    def get_channel_current(self, channel: int) -> float:
        if channel < 0 or channel >= 2:
            raise Exception("Invalid channel!")

        return float(self._device.query(f"CH{channel + 1}:CURR?"))

    def enable_channel(self, channel: int, enable: bool):
        if channel < 0 or channel >= 3:
            raise Exception("Invalid channel!")

        if enable:
            enable = "ON"
        else:
            enable = "OFF"

        self._device.write(f"OUTP CH{channel + 1},{enable}")
