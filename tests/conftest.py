import pytest

from unittest.mock import patch, AsyncMock


@pytest.fixture
def client_class():
    with patch('bleak.BleakClient') as client_class:
        yield client_class


@pytest.fixture
def client(client_class):
    client = AsyncMock()
    client_class.return_value = client

    connected = False

    async def is_connected():
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
