"""Device class"""
from binascii import hexlify
import logging

from .exceptions import PykulerskyException

_LOGGER = logging.getLogger(__name__)

CHARACTERISTIC_COMMAND_COLOR = "8d96b002-0002-64c2-0001-9acc4838521c"


class Light():
    """Represents one connected light"""

    def __init__(self, address, name=None):
        self.address = address
        self.name = name
        self.adapter = None
        self.device = None

    def connect(self, auto_reconnect=False):
        """Connect to this light"""
        import pygatt

        _LOGGER.info("Connecting to %s", self.address)

        self.adapter = pygatt.GATTToolBackend()
        try:
            self.adapter.start(reset_on_start=True)
            self.device = self.adapter.connect(
                self.address, auto_reconnect=auto_reconnect,
                address_type=pygatt.BLEAddressType.random)

        except pygatt.BLEError as ex:
            raise PykulerskyException() from ex

        _LOGGER.debug("Connected to %s", self.address)

    def disconnect(self):
        """Connect to this light"""
        import pygatt

        if self.adapter:
            try:
                self.adapter.stop()
            except pygatt.BLEError as ex:
                raise PykulerskyException() from ex
            self.adapter = None
            self.device = None

    def turn_on(self):
        """Turn on the light"""
        _LOGGER.info("Turning on %s", self.address)
        self._write(CHARACTERISTIC_COMMAND_COLOR, b'\x02\x00\x00\x00\xFF')
        _LOGGER.debug("Turned on %s", self.address)

    def turn_off(self):
        """Turn off the light"""
        _LOGGER.info("Turning off %s", self.address)
        self._write(CHARACTERISTIC_COMMAND_COLOR, b'\x32\xFF\xFF\xFF\xFF')
        _LOGGER.debug("Turned off %s", self.address)

    def set_color(self, r, g, b, w):
        """Set the color of the light

        Accepts red, green, blue, and white values from 0-255
        """
        for value in (r, g, b, w):
            if not 0 <= value <= 255:
                raise ValueError(
                    "Value {} is outside the valid range of 0-255")

        _LOGGER.info("Changing color of %s to #%02x%02x%02x%02x",
                     self.address, r, g, b, w)

        if r == 0 and g == 0 and b == 0 and w == 0:
            self.turn_off()
        else:
            color_string = bytes((r, g, b, w))

            value = b'\x02' + color_string
            self._write(CHARACTERISTIC_COMMAND_COLOR, value)
            _LOGGER.debug("Changed color of %s", self.address)

    def get_state(self):
        """Get the current state of the light"""
        color_string = self._read(CHARACTERISTIC_COMMAND_COLOR)

        on_off_value = int(color_string[0])

        r = int(color_string[1])
        g = int(color_string[2])
        b = int(color_string[3])
        w = int(color_string[4])

        if on_off_value == 0x02:
            is_on = True
        elif on_off_value == 0x32:
            is_on = False
        else:
            is_on = None

        state = LightState(is_on, (r, g, b, w))

        _LOGGER.info("Got state of %s: %s", self.address, state)

        return state

    def _read(self, uuid):
        """Internal method to read from the device"""
        import pygatt

        if not self.device:
            raise RuntimeError(
                "Light {} is not connected".format(self.address))

        _LOGGER.debug("Reading from characteristic %s", uuid)
        try:
            value = self.device.char_read(uuid)
        except pygatt.BLEError as ex:
            raise PykulerskyException() from ex
        _LOGGER.debug("Read 0x%s from characteristic %s", value.hex(), uuid)

        return value

    def _write(self, uuid, value):
        """Internal method to write to the device"""
        import pygatt

        if not self.device:
            raise RuntimeError(
                "Light {} is not connected".format(self.address))

        _LOGGER.debug("Writing 0x%s to characteristic %s", value.hex(), uuid)
        try:
            self.device.char_write(uuid, value)
        except pygatt.BLEError as ex:
            raise PykulerskyException() from ex
        _LOGGER.debug("Wrote 0x%s to characteristic %s", value.hex(), uuid)


class LightState():
    """Represents the current state of the light"""
    __slots__ = 'is_on', 'color',

    def __init__(self, is_on, color):
        """Create the state object"""
        self.is_on = is_on
        self.color = color

    def __repr__(self):
        """Return a string representation of the state object"""
        return "<LightState is_on='{}' color='{}'>".format(
            self.is_on, self.color)

    def __eq__(self, other):
        """Check for equality."""
        return self.is_on == other.is_on and self.color == other.color
