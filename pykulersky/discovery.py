"""Device discovery code"""
import logging

from .exceptions import PykulerskyException

_LOGGER = logging.getLogger(__name__)


def discover(timeout=10):
    """Returns nearby discovered bluetooth devices."""
    _LOGGER.info("Starting scan for local bluetooth devices")

    import pygatt
    adapter = pygatt.GATTToolBackend()

    devices = []
    try:
        adapter.start(reset_on_start=False)
        for device in adapter.scan(timeout=timeout):
            # There doesn't seem to be a way to distinguish these, so the user
            # will have to select the correct bluetooth device
            _LOGGER.info(
                "Discovered %s: %s", device['address'], device['name'])

            # Skip devices without a name. These devices include a name, and
            # removing other devices reduces the noise
            if device['name'] is not None:
                devices.append(device)
    except pygatt.BLEError as ex:
        raise PykulerskyException() from ex
    finally:
        try:
            adapter.stop()
        except pygatt.BLEError as ex:
            raise PykulerskyException() from ex

    _LOGGER.info("Scan complete")
    return devices
