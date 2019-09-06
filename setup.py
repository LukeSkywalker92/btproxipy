from setuptools import setup, find_packages
from pathlib import Path
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

CONFIG_DIR = os.path.join(Path.home(), '.config', 'btproxipy')
LOG_DIR = os.path.join(CONFIG_DIR, 'log')
SERVICE_DIR = os.path.join(Path.home(), '.local', 'share', 'systemd', 'user')


setup(name='btproxipy',
    version='0.1',
    description="Detects if a Bluetooth device is near by querying its RSSI value and executes commands when the device leaves or comes back.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/LukeSkywalker92/btproxipy',
    author='Lukas Scheffler',
    author_email='lukecodewalker92@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['PyBluez==0.22'],
    data_files=[(CONFIG_DIR, ['btproxipy.ini']),
                (LOG_DIR, []),
                (SERVICE_DIR, ['btproxipy.service'])],
    entry_points={
        'console_scripts': ['btproxipy=btproxipy.btproxipy:main']
    },
    classifiers=[
          "Programming Language :: Python :: 3",
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: End Users/Desktop",
          "Natural Language :: English",
          "License :: OSI Approved :: MIT License",
          "Operating System :: Linux",
      ],
    zip_safe=False)
