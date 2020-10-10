#!/usr/bin/env python
import pytest

import pygatt

from pykulersky import Light, PykulerskyException


def test_connect_disconnect(adapter, device):
    """Test the CLI."""
    light = Light("00:11:22")
    light.connect()

    adapter.start.assert_called_with(reset_on_start=False)
    adapter.connect.assert_called_with(
        "00:11:22", auto_reconnect=False,
        address_type=pygatt.BLEAddressType.random)

    light.disconnect()

    adapter.stop.assert_called_once()

    # Duplicate disconnect shouldn't call stop again
    light.disconnect()

    adapter.stop.assert_called_once()

    # Test auto reconnect
    light = Light("00:11:22")
    light.connect(auto_reconnect=True)

    adapter.start.assert_called_with(reset_on_start=False)
    adapter.connect.assert_called_with(
        "00:11:22", auto_reconnect=True,
        address_type=pygatt.BLEAddressType.random)


def test_get_color_not_connected(device):
    """Test the CLI."""
    light = Light("00:11:22")

    with pytest.raises(RuntimeError):
        light.get_color()


def test_set_color_not_connected(device):
    """Test the CLI."""
    light = Light("00:11:22")

    with pytest.raises(RuntimeError):
        light.set_color(255, 0, 0, 0)


def test_set_color(device):
    """Test the CLI."""
    light = Light("00:11:22")
    light.connect()

    light.set_color(255, 255, 255, 0)
    device.char_write.assert_called_with(
        '8d96b002-0002-64c2-0001-9acc4838521c',
        b'\x02\xFF\xFF\xFF\x00')

    light.set_color(64, 128, 192, 0)
    device.char_write.assert_called_with(
        '8d96b002-0002-64c2-0001-9acc4838521c',
        b'\x02\x40\x80\xC0\x00')

    light.set_color(0, 0, 0, 255)
    device.char_write.assert_called_with(
        '8d96b002-0002-64c2-0001-9acc4838521c',
        b'\x02\x00\x00\x00\xFF')

    # When called with all zeros, just turn off the light
    light.set_color(0, 0, 0, 0)
    device.char_write.assert_called_with(
        '8d96b002-0002-64c2-0001-9acc4838521c', b'\x32\xFF\xFF\xFF\xFF')

    with pytest.raises(ValueError):
        light.set_color(999, 999, 999, 999)


def test_get_color(device, mocker):
    """Test the CLI."""
    light = Light("00:11:22")
    light.connect()

    device.char_read.return_value = b'\x02\x00\x00\x00\xFF'
    color = light.get_color()
    device.char_read.assert_called_with('8d96b002-0002-64c2-0001-9acc4838521c')
    assert color == (0, 0, 0, 255)

    device.char_read.return_value = b'\x02\xFF\xFF\x00\x00'
    color = light.get_color()
    device.char_read.assert_called_with('8d96b002-0002-64c2-0001-9acc4838521c')
    assert color == (255, 255, 0, 0)

    device.char_read.return_value = b'\x32\xFF\xFF\xFF\x00'
    color = light.get_color()
    device.char_read.assert_called_with('8d96b002-0002-64c2-0001-9acc4838521c')
    assert color == (0, 0, 0, 0)


def test_exception_wrapping(device, adapter):
    """Test the CLI."""
    def raise_exception(*args, **kwargs):
        raise pygatt.BLEError("TEST")

    adapter.start.side_effect = raise_exception

    with pytest.raises(PykulerskyException):
        light = Light("00:11:22")
        light.connect()

    adapter.start.side_effect = None
    adapter.stop.side_effect = raise_exception

    with pytest.raises(PykulerskyException):
        light = Light("00:11:22")
        light.connect()
        light.disconnect()

    device.char_write.side_effect = raise_exception

    with pytest.raises(PykulerskyException):
        light = Light("00:11:22")
        light.connect()
        light.set_color(0, 0, 0, 0)

    device.char_read.side_effect = raise_exception

    with pytest.raises(PykulerskyException):
        light = Light("00:11:22")
        light.connect()
        light.get_color()
