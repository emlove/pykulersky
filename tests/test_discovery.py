#!/usr/bin/env python
import pygatt
import pytest

from pykulersky import discover, PykulerskyException


def test_discover_devices(adapter):
    """Test the CLI."""
    def scan(*args, **kwargs):
        """Simulate a scanning response"""
        return [
            {
                'address': 'AA:BB:CC:11:22:33',
                'name': 'LEDBlue-CC112233 ',
            },
            {
                'address': 'AA:BB:CC:44:55:66',
                'name': 'LEDBlue-CC445566 ',
            },
            {
                'address': 'DD:EE:FF:11:22:33',
                'name': 'Other',
            },
            {
                'address': 'DD:EE:FF:44:55:66',
                'name': None,
            },
        ]

    adapter.scan.side_effect = scan

    devices = discover(15)

    assert devices[0].address == 'AA:BB:CC:11:22:33'
    assert devices[0].name == 'LEDBlue-CC112233'
    assert devices[1].address == 'AA:BB:CC:44:55:66'
    assert devices[1].name == 'LEDBlue-CC445566'

    adapter.start.assert_called_with(reset_on_start=False)
    adapter.scan.assert_called_with(timeout=15)
    adapter.stop.assert_called_once()


def test_exception_wrapping(adapter):
    """Test the CLI."""
    def raise_exception(*args, **kwargs):
        raise pygatt.BLEError("TEST")

    adapter.scan.side_effect = raise_exception

    with pytest.raises(PykulerskyException):
        discover()

    adapter.scan.side_effect = None
    adapter.stop.side_effect = raise_exception

    with pytest.raises(PykulerskyException):
        discover()
