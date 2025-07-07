#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

from pykulersky import __author__, __email__, __version__

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'Click>=7.0',
    'bleak>=1.0.1',
]

test_requirements = ['pytest>=3', ]

setup(
    author=__author__,
    author_email=__email__,
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    description=(
        "Library to control Brightech Kuler Sky Bluetooth LED smart lamps"),
    entry_points={
        'console_scripts': [
            'pykulersky=pykulersky.cli:main',
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme,
    include_package_data=True,
    keywords='pykulersky',
    name='pykulersky',
    packages=find_packages(include=['pykulersky', 'pykulersky.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/emlove/pykulersky',
    version=__version__,
    zip_safe=False,
)
