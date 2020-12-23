#!/usr/bin/env python
import pytest

import bleak

from pykulersky import discover, PykulerskyException


@pytest.mark.asyncio
async def test_discover_devices(scanner, client_class):
    """Test the CLI."""
    async def scan(*args, **kwargs):
        """Simulate a scanning response"""
        return [
            bleak.backends.device.BLEDevice(
                'AA:BB:CC:11:22:33',
                'Living Room',
                uuids=[
                    "8d96a001-0002-64c2-0001-9acc4838521c",
                ],
                manufacturer_data={}
            ),
            bleak.backends.device.BLEDevice(
                address='AA:BB:CC:44:55:66',
                name='Bedroom',
                uuids=[
                    "8d96a001-0002-64c2-0001-9acc4838521c",
                ],
                manufacturer_data={}
            ),
            bleak.backends.device.BLEDevice(
                address='DD:EE:FF:11:22:33',
                name='Other',
                uuids=[
                    "0000fe9f-0000-1000-8000-00805f9b34fb",
                ],
                manufacturer_data={}
            ),
        ]

    scanner.discover.side_effect = scan

    devices = await discover(15)

    assert len(devices) == 2
    assert devices[0].address == 'AA:BB:CC:11:22:33'
    assert devices[0].name == 'Living Room'
    assert devices[1].address == 'AA:BB:CC:44:55:66'
    assert devices[1].name == 'Bedroom'

    scanner.discover.assert_called_once()


@pytest.mark.asyncio
async def test_exception_wrapping(scanner):
    """Test the CLI."""
    async def raise_exception(*args, **kwargs):
        raise bleak.exc.BleakError("TEST")

    scanner.discover.side_effect = raise_exception

    with pytest.raises(PykulerskyException):
        await discover()
