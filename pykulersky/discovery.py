"""Device discovery code"""
import asyncio
import logging

from .light import Light
from .exceptions import PykulerskyException

_LOGGER = logging.getLogger(__name__)

EXPECTED_SERVICES = [
    "8d96a001-0002-64c2-0001-9acc4838521c",
]


async def discover(timeout=10):
    """Returns nearby discovered lights."""
    import bleak

    _LOGGER.info("Starting scan for local devices")

    lights = []
    try:
        devices = await asyncio.wait_for(
            bleak.BleakScanner.discover(service_uuids=EXPECTED_SERVICES),
            timeout)
    except Exception as ex:
        raise PykulerskyException() from ex
    for device in devices:
        lights.append(Light(device.address, device.name))

    _LOGGER.info("Scan complete")
    return lights
