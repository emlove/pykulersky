import pytest
import sys

if sys.version_info[:2] < (3, 8):
    from asynctest import patch, CoroutineMock, MagicMock as AsyncMock
else:
    from unittest.mock import patch, AsyncMock


@pytest.fixture
def client_class():
    with patch('bleak.BleakClient') as client_class:
        yield client_class


@pytest.fixture
def client(client_class):
    client = AsyncMock()
    client_class.return_value = client

    if sys.version_info[:2] < (3, 8):
        client.read_gatt_char = CoroutineMock()
        client.write_gatt_char = CoroutineMock()

    connected = False

    async def is_connected():
        nonlocal connected
        return connected

    async def connect():
        nonlocal connected
        connected = True

    async def disconnect():
        nonlocal connected
        connected = False

    client.is_connected.side_effect = is_connected
    client.connect.side_effect = connect
    client.disconnect.side_effect = disconnect

    yield client


@pytest.fixture
def scanner():
    with patch('bleak.BleakScanner') as scanner:
        yield scanner
