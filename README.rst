==========
pykulersky
==========


.. image:: https://img.shields.io/pypi/v/pykulersky.svg
        :target: https://pypi.python.org/pypi/pykulersky

.. image:: https://github.com/emlove/pykulersky/workflows/tests/badge.svg
        :target: https://github.com/emlove/pykulersky/actions

.. image:: https://coveralls.io/repos/emlove/pykulersky/badge.svg
        :target: https://coveralls.io/r/emlove/pykulersky


Library to control Brightech Kuler Sky Bluetooth LED smart lamps

* Free software: Apache Software License 2.0


Features
--------

* Discover nearby bluetooth devices
* Get light color
* Set light color


Command line usage
------------------
pykulersky ships with a command line tool that exposes the features of the library.

.. code-block:: console

    $ pykulersky discover
    INFO:pykulersky.discovery:Starting scan for local devices
    INFO:pykulersky.discovery:Discovered AA:BB:CC:00:11:22: Living Room
    INFO:pykulersky.discovery:Discovered AA:BB:CC:33:44:55: Bedroom
    INFO:pykulersky.discovery:Scan complete
    AA:BB:CC:00:11:22: Living Room
    AA:BB:CC:33:44:55: Bedroom

    $ pykulersky get-color AA:BB:CC:00:11:22
    INFO:pykulersky.light:Connecting to AA:BB:CC:00:11:22
    INFO:pykulersky.light:Got color of AA:BB:CC:00:11:22: (0, 0, 0, 255)'>
    000000ff

    $ pykulersky set-color AA:BB:CC:00:11:22 ff000000
    INFO:pykulersky.light:Connecting to AA:BB:CC:00:11:22
    INFO:pykulersky.light:Changing color of AA:BB:CC:00:11:22 to #ff000000

    $ pykulersky set-color AA:BB:CC:00:11:22 000000ff
    INFO:pykulersky.light:Connecting to AA:BB:CC:00:11:22
    INFO:pykulersky.light:Changing color of AA:BB:CC:00:11:22 to #000000ff


Usage
-----

Discover nearby bluetooth devices

.. code-block:: python

    import asyncio
    import pykulersky


    async def main():
        lights = await pykulersky.discover(timeout=5)

        for light in lights:
            print("Address: {} Name: {}".format(light.address, light.name))

    asyncio.get_event_loop().run_until_complete(main())


Turn a light on and off

.. code-block:: python

    import asyncio
    import pykulersky


    async def main():
        address = "AA:BB:CC:00:11:22"

        light = pykulersky.Light(address)

        try:
            await light.connect()
            await light.set_color(0, 0, 0, 255)

            await asyncio.sleep(5)

            await light.set_color(0, 0, 0, 0)
        finally:
            await light.disconnect()

    asyncio.get_event_loop().run_until_complete(main())


Change the light color

.. code-block:: python

    import asyncio
    import pykulersky


    async def main():
        address = "AA:BB:CC:00:11:22"

        light = pykulersky.Light(address)

        try:
            await light.connect()
            while True:
                await light.set_color(255, 0, 0, 0) # Red
                await asyncio.sleep(1)
                await light.set_color(0, 255, 0, 0) # Green
                await asyncio.sleep(1)
                await light.set_color(0, 0, 0, 255) # White
                await asyncio.sleep(1)
        finally:
            await light.disconnect()

    asyncio.get_event_loop().run_until_complete(main())


Get the light color

.. code-block:: python

    import asyncio
    import pykulersky


    async def main():
        address = "AA:BB:CC:00:11:22"

        light = pykulersky.Light(address)

        try:
            await light.connect()
            color = await light.get_color()
            print(color)
        finally:
            await light.disconnect()

    asyncio.get_event_loop().run_until_complete(main())


Changelog
---------
0.6.0 (2025-07-07)
~~~~~~~~~~~~~~~~~~
- Update to support bleak 1.0

0.5.8 (2025-01-24)
~~~~~~~~~~~~~~~~~~
- Fix missing awaits

0.5.7 (2025-01-24)
~~~~~~~~~~~~~~~~~~
- Lower noisy log priorities

0.5.6 (2025-01-24)
~~~~~~~~~~~~~~~~~~
- Allow bleak device to be passed through

0.5.5 (2023-04-07)
~~~~~~~~~~~~~~~~~~
- Support CI for bleak 0.20

0.5.4 (2022-05-03)
~~~~~~~~~~~~~~~~~~
- Unpin test dependencies

0.5.3 (2021-11-23)
~~~~~~~~~~~~~~~~~~
- Support CI for bleak 0.13

0.5.2 (2021-03-04)
~~~~~~~~~~~~~~~~~~
- Use built-in asyncmock for Python 3.8+

0.5.1 (2020-12-23)
~~~~~~~~~~~~~~~~~~
- Include default timeout on all API calls

0.5.0 (2020-12-19)
~~~~~~~~~~~~~~~~~~
- Refactor from pygatt to bleak for async interface

0.4.0 (2020-11-11)
~~~~~~~~~~~~~~~~~~
- Rename discover method to make behavior clear

0.3.1 (2020-11-10)
~~~~~~~~~~~~~~~~~~
- Fix connected status after broken connection

0.3.0 (2020-11-10)
~~~~~~~~~~~~~~~~~~
- Add workaround for firmware bug

0.2.0 (2020-10-14)
~~~~~~~~~~~~~~~~~~
- Remove thread-based auto_reconnect

0.1.1 (2020-10-13)
~~~~~~~~~~~~~~~~~~
- Always raise PykulerskyException

0.1.0 (2020-10-09)
~~~~~~~~~~~~~~~~~~
- Initial release

0.0.1 (2020-10-09)
~~~~~~~~~~~~~~~~~~
- Fork from pyzerproc


Credits
-------

- Thanks to `Uri Shaked`_ for an incredible guide to `Reverse Engineering a Bluetooth Lightbulb`_.

- This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _`Uri Shaked`: https://medium.com/@urish
.. _`Reverse Engineering a Bluetooth Lightbulb`: https://medium.com/@urish/reverse-engineering-a-bluetooth-lightbulb-56580fcb7546
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
