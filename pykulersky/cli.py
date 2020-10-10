"""Console script for pykulersky."""
import sys
from binascii import hexlify
import click
import logging

import pykulersky


@click.group()
@click.option('-v', '--verbose', count=True,
              help="Pass once to enable pykulersky debug logging. Pass twice "
                   "to also enable pygatt debug logging.")
def main(verbose):
    """Console script for pykulersky."""
    logging.basicConfig()
    logging.getLogger('pykulersky').setLevel(logging.INFO)
    if verbose >= 1:
        logging.getLogger('pykulersky').setLevel(logging.DEBUG)
    if verbose >= 2:
        logging.getLogger('pygatt').setLevel(logging.DEBUG)


@main.command()
def discover():
    """Discover nearby bluetooth devices"""
    devices = pykulersky.discover()
    for device in devices:
        click.echo("{}: {}".format(device["address"], device["name"]))

    return 0


@main.command()
@click.argument('address')
def get_color(address):
    """Get the current color of the light"""
    light = pykulersky.Light(address)

    try:
        light.connect()
        color = light.get_color()
        click.echo(hexlify(bytes(color)))
    finally:
        light.disconnect()
    return 0


@main.command()
@click.argument('address')
@click.argument('color')
def set_color(address, color):
    """Set the light with the given MAC address to an RRGGBBWW hex color"""
    light = pykulersky.Light(address)

    r, g, b, w = tuple(int(color[i:i+2], 16) for i in (0, 2, 4, 6))

    try:
        light.connect()
        light.set_color(r, g, b, w)
    finally:
        light.disconnect()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
