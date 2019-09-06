# btproxipy

## Requirements

This program needs `bluetooth` to be installed.

Debian/Ubuntu:

``` bash
sudo apt-get install bluetooth
```

Arch Linux:

``` bash
pacman -S bluez bluez-utils
systemctl enable bluetooth.service
```

## Installation

``` bash
pip install btproxipy
```

Edit `~/.config/btproxipy/btproxipy.ini` to your needs.

``` bash
systemctl --user enable btproxipy
systemctl --user start btproxipy
```
