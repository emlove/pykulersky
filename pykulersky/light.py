"""Device class"""
import logging

from .exceptions import PykulerskyException

_LOGGER = logging.getLogger(__name__)

CHARACTERISTIC_COMMAND_COLOR = "8d96b002-0002-64c2-0001-9acc4838521c"


class Light():
    """Represents one connected light"""

    def __init__(self, address, name=None):
        self._address = address
        self._name = name
        self._adapter = None
        self._device = None

    def connect(self):
        """Open the connection to this light."""
        import pygatt

        if self.connected:
            return

        _LOGGER.info("Connecting to %s", self.address)

        self._adapter = pygatt.GATTToolBackend()
        try:
            self._adapter.start(reset_on_start=False)
            self._device = self._adapter.connect(
                self.address, address_type=pygatt.BLEAddressType.random)
        except pygatt.BLEError as ex:
            self._adapter = None
            self._device = None
            raise PykulerskyException() from ex

        _LOGGER.debug("Connected to %s", self.address)

    def disconnect(self):
        """Close the connection to this light."""
        import pygatt

        if self._adapter:
            try:
                self._adapter.stop()
            except pygatt.BLEError as ex:
                raise PykulerskyException() from ex
            finally:
                self._adapter = None
                self._device = None

    @property
    def address(self):
        """Return the mac address of this light."""
        return self._address

    @property
    def name(self):
        """Return the discovered name of this light."""
        return self._name

    @property
    def connected(self):
        """Returns true if the light is connected."""
        return self._device is not None

    def set_color(self, r, g, b, w):
        """Set the color of the light

        Accepts red, green, blue, and white values from 0-255
        """
        for value in (r, g, b, w):
            if not 0 <= value <= 255:
                raise ValueError(
                    "Value {} is outside the valid range of 0-255")

        old_color = self.get_color()
        was_on = max(old_color) > 0

        _LOGGER.info("Changing color of %s to #%02x%02x%02x%02x",
                     self.address, r, g, b, w)

        if r == 0 and g == 0 and b == 0 and w == 0:
            color_string = b'\x32\xFF\xFF\xFF\xFF'
        else:
            if not was_on and w > 0:
                # These lights have a firmware bug. When turning the light on
                # from off, the white channel is broken until it is first set
                # to zero. If the light was off, first apply the color with a
                # zero white channel, then write the actual color we want.
                color_string = b'\x02' + bytes((r, g, b, 0))
                self._write(CHARACTERISTIC_COMMAND_COLOR, color_string)
            color_string = b'\x02' + bytes((r, g, b, w))

        self._write(CHARACTERISTIC_COMMAND_COLOR, color_string)
        _LOGGER.debug("Changed color of %s", self.address)

    def get_color(self):
        """Get the current color of the light"""
        color_string = self._read(CHARACTERISTIC_COMMAND_COLOR)

        on_off_value = int(color_string[0])

        r = int(color_string[1])
        g = int(color_string[2])
        b = int(color_string[3])
        w = int(color_string[4])

        if on_off_value == 0x32:
            color = (0, 0, 0, 0)
        else:
            color = (r, g, b, w)

        _LOGGER.info("Got color of %s: %s", self.address, color)

        return color

    def _read(self, uuid):
        """Internal method to read from the device"""
        import pygatt

        if not self.connected:
            raise PykulerskyException(
                "Light {} is not connected".format(self.address))

        _LOGGER.debug("Reading from characteristic %s", uuid)
        try:
            value = self._device.char_read(uuid)
        except pygatt.BLEError as ex:
            raise PykulerskyException() from ex
        _LOGGER.debug("Read 0x%s from characteristic %s", value.hex(), uuid)

        return value

    def _write(self, uuid, value):
        """Internal method to write to the device"""
        import pygatt

        if not self.connected:
            raise PykulerskyException(
                "Light {} is not connected".format(self.address))

        _LOGGER.debug("Writing 0x%s to characteristic %s", value.hex(), uuid)
        try:
            self._device.char_write(uuid, value)
        except pygatt.BLEError as ex:
            raise PykulerskyException() from ex
        _LOGGER.debug("Wrote 0x%s to characteristic %s", value.hex(), uuid)
