#!/usr/bin/env python
import asyncio
import pytest

import bleak

from pykulersky import Light, PykulerskyException
from .conftest import AsyncMock


@pytest.mark.asyncio
async def test_connect_disconnect(client_class, client):
    """Test connecting and disconnecting."""
    light = Light("00:11:22")

    client_class.assert_called_with("00:11:22")

    await light.connect()
    client.connect.assert_called_once()

    await light.disconnect()
    client.disconnect.assert_called_once()


@pytest.mark.asyncio
async def test_connect_exception(client):
    """Test an exception while connecting."""
    light = Light("00:11:22")

    client.connect.side_effect = bleak.exc.BleakError("TEST")

    with pytest.raises(PykulerskyException):
        await light.connect()


@pytest.mark.asyncio
async def test_disconnect_exception(client):
    """Test an exception while disconnecting."""
    light = Light("00:11:22")
    await light.connect()

    client.disconnect.side_effect = bleak.exc.BleakError("TEST")

    with pytest.raises(PykulerskyException):
        await light.disconnect()


@pytest.mark.asyncio
async def test_is_connected(client):
    """Test an exception while connecting."""
    light = Light("00:11:22")

    client.is_connected.side_effect = asyncio.TimeoutError("TEST")

    assert not await light.is_connected()


@pytest.mark.asyncio
async def test_get_color(client):
    """Test getting light color."""
    light = Light("00:11:22")
    await light.connect()

    client.read_gatt_char.return_value = bytearray(b'\x02\x00\x00\x00\xFF')
    color = await light.get_color()
    client.read_gatt_char.assert_called_with(
        '8d96b002-0002-64c2-0001-9acc4838521c')
    assert color == (0, 0, 0, 255)

    client.read_gatt_char.return_value = bytearray(b'\x02\xFF\xFF\x00\x00')
    color = await light.get_color()
    client.read_gatt_char.assert_called_with(
        '8d96b002-0002-64c2-0001-9acc4838521c')
    assert color == (255, 255, 0, 0)

    client.read_gatt_char.return_value = bytearray(b'\x32\xFF\xFF\xFF\x00')
    color = await light.get_color()
    client.read_gatt_char.assert_called_with(
        '8d96b002-0002-64c2-0001-9acc4838521c')
    assert color == (0, 0, 0, 0)


@pytest.mark.asyncio
async def test_set_color(client):
    """Test setting light color."""
    light = Light("00:11:22")
    await light.connect()

    client.read_gatt_char.return_value = bytearray(b'\x02\xFF\xFF\xFF\x00')
    await light.set_color(255, 255, 255, 0)
    client.write_gatt_char.assert_called_with(
        '8d96b002-0002-64c2-0001-9acc4838521c',
        b'\x02\xFF\xFF\xFF\x00')

    client.read_gatt_char.return_value = bytearray(b'\x02\xFF\xFF\xFF\x00')
    await light.set_color(64, 128, 192, 0)
    client.write_gatt_char.assert_called_with(
        '8d96b002-0002-64c2-0001-9acc4838521c',
        b'\x02\x40\x80\xC0\x00')

    client.read_gatt_char.return_value = bytearray(b'\x02\xFF\xFF\xFF\x00')
    await light.set_color(0, 0, 0, 255)
    client.write_gatt_char.assert_called_with(
        '8d96b002-0002-64c2-0001-9acc4838521c',
        b'\x02\x00\x00\x00\xFF')

    # When called with all zeros, just turn off the light
    client.read_gatt_char.return_value = bytearray(b'\x02\xFF\xFF\xFF\x00')
    await light.set_color(0, 0, 0, 0)
    client.write_gatt_char.assert_called_with(
        '8d96b002-0002-64c2-0001-9acc4838521c',
        b'\x32\xFF\xFF\xFF\xFF')

    # Turn on only the RGB channels
    client.read_gatt_char.return_value = bytearray(b'\x32\xFF\xFF\xFF\xFF')
    await light.set_color(255, 255, 255, 0)
    client.write_gatt_char.assert_called_with(
        '8d96b002-0002-64c2-0001-9acc4838521c',
        b'\x02\xFF\xFF\xFF\x00')
    client.reset_mock()

    # Turn on white channel when previously off (test firmware workaround)
    client.read_gatt_char.return_value = bytearray(b'\x32\xFF\xFF\xFF\xFF')
    await light.set_color(255, 255, 255, 255)
    client.write_gatt_char.call_args_list[0][0] == (
        '8d96b002-0002-64c2-0001-9acc4838521c', b'\x02\xFF\xFF\xFF\x00')
    client.write_gatt_char.call_args_list[0][0] == (
        '8d96b002-0002-64c2-0001-9acc4838521c', b'\x02\xFF\xFF\xFF\x00')
    client.reset_mock()

    with pytest.raises(ValueError):
        await light.set_color(999, 999, 999, 999)


@pytest.mark.asyncio
async def test_exception_wrapping(client):
    """Test that exceptions are wrapped."""
    light = Light("00:11:22")
    await light.connect()

    client.is_connected.side_effect = bleak.exc.BleakError("TEST")

    with pytest.raises(PykulerskyException):
        await light.is_connected()

    client.write_gatt_char.side_effect = bleak.exc.BleakError("TEST")

    with pytest.raises(PykulerskyException):
        await light.set_color(255, 255, 255, 255)

    light._do_set_color = AsyncMock()
    light._do_set_color.side_effect = asyncio.TimeoutError("Mock timeout")

    with pytest.raises(PykulerskyException):
        await light.set_color(255, 255, 255, 255)

    client.read_gatt_char.side_effect = bleak.exc.BleakError("TEST")

    with pytest.raises(PykulerskyException):
        await light.get_color()

    light._do_get_color = AsyncMock()
    light._do_get_color.side_effect = asyncio.TimeoutError("Mock timeout")

    with pytest.raises(PykulerskyException):
        await light.get_color()
