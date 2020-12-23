"""Device class"""
import asyncio
import logging

from .exceptions import PykulerskyException

_LOGGER = logging.getLogger(__name__)

CHARACTERISTIC_COMMAND_COLOR = "8d96b002-0002-64c2-0001-9acc4838521c"

# Default to a 5s timeout on remote calls
DEFAULT_TIMEOUT = 5


class Light():
    """Represents one connected light"""

    def __init__(self, address, name=None, *args,
                 default_timeout=DEFAULT_TIMEOUT):
        import bleak

        self._address = address
        self._name = name
        self._client = bleak.BleakClient(self._address)
        self._default_timeout = DEFAULT_TIMEOUT

    @property
    def address(self):
        """Return the mac address of this light."""
        return self._address

    @property
    def name(self):
        """Return the discovered name of this light."""
        return self._name

    async def is_connected(self, *args, timeout=None):
        """Returns true if the light is connected."""
        try:
            return await asyncio.wait_for(
                self._client.is_connected(),
                self._default_timeout if timeout is None else timeout)
        except asyncio.TimeoutError:
            return False
        except Exception as ex:
            raise PykulerskyException() from ex

    async def connect(self, *args, timeout=None):
        """Connect to this light"""
        _LOGGER.debug("Connecting to %s", self._address)

        try:
            await asyncio.wait_for(
                self._client.connect(),
                self._default_timeout if timeout is None else timeout)
        except Exception as ex:
            raise PykulerskyException() from ex

        _LOGGER.debug("Connected to %s", self._address)

    async def disconnect(self, *args, timeout=None):
        """Close the connection to the light."""
        _LOGGER.debug("Disconnecting from %s", self._address)
        try:
            await asyncio.wait_for(
                self._client.disconnect(),
                self._default_timeout if timeout is None else timeout)
        except Exception as ex:
            raise PykulerskyException() from ex
        _LOGGER.debug("Disconnected from %s", self._address)

    async def _do_set_color(self, r, g, b, w):
        """Set the color of the light"""
        for value in (r, g, b, w):
            if not 0 <= value <= 255:
                raise ValueError(
                    "Value {} is outside the valid range of 0-255")

        old_color = await self._do_get_color()
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

        await self._write(CHARACTERISTIC_COMMAND_COLOR, color_string)
        _LOGGER.debug("Changed color of %s", self.address)

    async def set_color(self, r, g, b, w, *args, timeout=None):
        """Set the color of the light

        Accepts red, green, blue, and white values from 0-255
        """
        try:
            await asyncio.wait_for(
                self._do_set_color(r, g, b, w),
                self._default_timeout if timeout is None else timeout)
        except asyncio.TimeoutError as ex:
            raise PykulerskyException() from ex

    async def _do_get_color(self):
        """Get the current color of the light"""
        color_string = await self._read(CHARACTERISTIC_COMMAND_COLOR)

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

    async def get_color(self, *args, timeout=None):
        """Get the current color of the light"""
        try:
            return await asyncio.wait_for(
                self._do_get_color(),
                self._default_timeout if timeout is None else timeout)
        except asyncio.TimeoutError as ex:
            raise PykulerskyException() from ex

    async def _read(self, uuid):
        """Internal method to read from the device"""
        _LOGGER.debug("Reading from characteristic %s", uuid)
        try:
            value = await self._client.read_gatt_char(uuid)
        except Exception as ex:
            raise PykulerskyException() from ex
        _LOGGER.debug("Read 0x%s from characteristic %s", value.hex(), uuid)

        return value

    async def _write(self, uuid, value):
        """Internal method to write to the device"""
        _LOGGER.debug("Writing 0x%s to characteristic %s", value.hex(), uuid)
        try:
            await self._client.write_gatt_char(uuid, bytearray(value))
        except Exception as ex:
            raise PykulerskyException() from ex
        _LOGGER.debug("Wrote 0x%s to characteristic %s", value.hex(), uuid)
