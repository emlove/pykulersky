#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

import pyzerproc

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = ['Click>=7.0', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author=pyzerproc.__author__,
    author_email=pyzerproc.__email__,
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Asyncio library to control Zerproc Bluetooth LED smart string lights",
    entry_points={
        'console_scripts': [
            'pyzerproc=pyzerproc.cli:main',
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme,
    include_package_data=True,
    keywords='pyzerproc',
    name='pyzerproc',
    packages=find_packages(include=['pyzerproc', 'pyzerproc.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/emlove/pyzerproc',
    version=pyzerproc.__version__,
    zip_safe=False,
)
