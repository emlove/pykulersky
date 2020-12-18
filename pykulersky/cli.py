"""Console script for pykulersky."""
import asyncio
import sys
from binascii import hexlify
import click
import logging

import pykulersky


@click.group()
@click.option('-v', '--verbose', count=True,
              help="Pass once to enable pykulersky debug logging. Pass twice "
                   "to also enable bleak debug logging.")
def main(verbose):
    """Console script for pykulersky."""
    logging.basicConfig()
    logging.getLogger('pykulersky').setLevel(logging.INFO)
    if verbose >= 1:
        logging.getLogger('pykulersky').setLevel(logging.DEBUG)
    if verbose >= 2:
        logging.getLogger('bleak').setLevel(logging.DEBUG)


@main.command()
def discover():
    """Discover nearby lights"""
    async def run():
        lights = await pykulersky.discover()
        if not lights:
            click.echo("No nearby lights found")
        for light in lights:
            click.echo(light.address)

    asyncio.get_event_loop().run_until_complete(run())
    return 0


@main.command()
@click.argument('address')
def get_color(address):
    """Get the current color of the light"""
    async def run():
        light = pykulersky.Light(address)

        try:
            await light.connect()
            color = await light.get_color()
            click.echo(hexlify(bytes(color)))
        finally:
            await light.disconnect()

    asyncio.get_event_loop().run_until_complete(run())
    return 0


@main.command()
@click.argument('address')
@click.argument('color')
def set_color(address, color):
    """Set the light with the given MAC address to an RRGGBBWW hex color"""
    async def run():
        light = pykulersky.Light(address)

        r, g, b, w = tuple(int(color[i:i+2], 16) for i in (0, 2, 4, 6))

        try:
            await light.connect()
            await light.set_color(r, g, b, w)
        finally:
            await light.disconnect()

    asyncio.get_event_loop().run_until_complete(run())
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
