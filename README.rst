==========
pykulersky
==========


.. image:: https://img.shields.io/pypi/v/pykulersky.svg
        :target: https://pypi.python.org/pypi/pykulersky

.. image:: https://travis-ci.com/emlove/pykulersky.svg?branch=master
        :target: https://travis-ci.com/github/emlove/pykulersky

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

    import pykulersky

    lights = pykulersky.discover(timeout=30)

    for light in lights:
        print("Address: {} Name: {}".format(light['address'], light['name']))


Turn a light on and off

.. code-block:: python

    import pykulersky
    import time

    address = "AA:BB:CC:00:11:22"

    light = pykulersky.Light(address)

    try:
        light.connect(auto_reconnect=True)
        light.set_color(0, 0, 0, 255)

        time.sleep(5)

        light.set_color(0, 0, 0, 0)
    finally:
        light.disconnect()


Change the light color

.. code-block:: python

    import pykulersky
    import time

    address = "AA:BB:CC:00:11:22"

    light = pykulersky.Light(address)

    try:
        light.connect()

        while True:
            light.set_color(255, 0, 0, 0) # Red
            time.sleep(1)
            light.set_color(0, 255, 0, 0) # Green
            time.sleep(1)
            light.set_color(0, 0, 0, 255) # White
    finally:
        light.disconnect()


Get the light color

.. code-block:: python

    import pykulersky
    import time

    address = "AA:BB:CC:00:11:22"

    light = pykulersky.Light(address)

    try:
        light.connect()

        color = light.get_color()

        print(color)
    finally:
        light.disconnect()


Changelog
---------
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
