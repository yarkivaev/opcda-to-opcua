"""
Setup script for opcda_to_mqtt package.
"""
from setuptools import setup, find_packages

setup(
    name='opcda_to_mqtt',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'paho-mqtt==1.6.1',
    ],
    entry_points={
        'console_scripts': [
            'opcda-mqtt=opcda_to_mqtt.app.main:main',
        ],
    },
)
