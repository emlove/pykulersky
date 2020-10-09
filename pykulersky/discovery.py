"""Device discovery code"""
import logging

from .light import Light
from .exceptions import PykulerskyException

_LOGGER = logging.getLogger(__name__)


def discover(timeout=10):
    """Returns nearby discovered lights."""
    _LOGGER.info("Starting scan for local devices")

    import pygatt
    adapter = pygatt.GATTToolBackend()

    lights = []
    try:
        adapter.start(reset_on_start=False)
        for device in adapter.scan(timeout=timeout):
            # Improvements welcome
            if device['name'] and device['name'].startswith('LEDBlue-'):
                _LOGGER.info(
                    "Discovered %s: %s", device['address'], device['name'])
                lights.append(
                    Light(device['address'], device['name'].strip()))
    except pygatt.BLEError as ex:
        raise PykulerskyException() from ex
    finally:
        try:
            adapter.stop()
        except pygatt.BLEError as ex:
            raise PykulerskyException() from ex

    _LOGGER.info("Scan complete")
    return lights
