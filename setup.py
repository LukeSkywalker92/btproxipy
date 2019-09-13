from setuptools import setup, find_packages
from pathlib import Path
import os
from shutil import copyfile

with open("README.md", "r") as fh:
    long_description = fh.read()

CONFIG_DIR = os.path.join(Path.home(), '.config', 'btproxipy')
LOG_DIR = os.path.join(CONFIG_DIR, 'log')
CONFIG_PATH = os.path.join(CONFIG_DIR, 'btproxipy.ini')
SERVICE_DIR = os.path.join(Path.home(), '.local', 'share', 'systemd', 'user')
SERVICE_PATH = os.path.join(SERVICE_DIR, 'btproxipy.service')

config = os.path.join(os.path.expanduser('~'), '.my_config')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
if not os.path.exists(CONFIG_PATH):
    copyfile('btproxipy.ini', CONFIG_PATH)
if not os.path.exists(SERVICE_DIR):
    os.makedirs(SERVICE_DIR)
if not os.path.exists(SERVICE_PATH):
    copyfile('btproxipy.service', SERVICE_PATH)

setup(name='btproxipy',
    version='0.9',
    description="Detects if a Bluetooth device is near by querying its RSSI value and executes commands when the device leaves or comes back.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/LukeSkywalker92/btproxipy',
    author='Lukas Scheffler',
    author_email='lukecodewalker92@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['PyBluez==0.22'],
    entry_points={
        'console_scripts': ['btproxipy=btproxipy.btproxipy:main']
    },
    classifiers=[
          "Programming Language :: Python :: 3",
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: End Users/Desktop",
          "Natural Language :: English",
          "License :: OSI Approved :: MIT License",
          "Operating System :: POSIX :: Linux",
      ],
    zip_safe=False)
