# -*- coding: utf-8 -*-
"""
Setup script for opcda_to_opcua package.
"""
from setuptools import setup, find_packages

setup(
    name='opcda_to_opcua',
    version='1.0.0',
    description='OPC-DA to OPC-UA Bridge',
    author='Your Name',
    packages=find_packages(exclude=['tests', 'tests.*']),
    # Dependencies installed manually (old pip can't parse complex specifiers)
    # See requirements.txt: opcua, OpenOPC, pywin32
    install_requires=[],
    entry_points={
        'console_scripts': [
            'opcda-bridge=opcda_to_opcua.app.main:main',
        ],
    },
    python_requires='>=3.4',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.4',
        'Topic :: System :: Networking',
    ],
)
