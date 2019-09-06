from btproxipy.bt_rssi import BluetoothRSSI
import datetime
import time
import threading
import sys
import subprocess
import configparser
import os
from pathlib import Path
import logging
import logging.handlers

CONFIG_PATH = os.path.join(Path.home(), '.config', 'btproxipy', 'btproxipy.ini')
LOG_PATH = os.path.join(Path.home(), '.config', 'btproxipy', 'log', 'btproxipy.log')


config = configparser.ConfigParser()
config.read(CONFIG_PATH)

DEBUG = config['CONFIG'].getboolean('debug')
THRESHOLD = config['CONFIG'].getint('threshold')
SLEEP = config['CONFIG'].getint('interval')
AWAY_THRESHOLD = config['CONFIG'].getint('awaycount')
HERE_COMMAND = config['CONFIG']['here_command']
AWAY_COMMAND = config['CONFIG']['away_command']
BT_ADDR = config['CONFIG']['bt_adress']

level = logging.INFO
if DEBUG:
    level = logging.DEBUG

logging.basicConfig(
    level=level,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.handlers.RotatingFileHandler(LOG_PATH, maxBytes=99999, backupCount=5),
        logging.StreamHandler()
    ])


device_present = False
away_count = 0


def here_callback():
    global device_present
    global away_count
    away_count = 0
    if device_present is False:
        device_present=True
        logging.info('Device present. Running ' + HERE_COMMAND)
        subprocess.run(HERE_COMMAND, shell=True)


def away_callback(disconnect):
    global device_present
    global away_count
    away_count += 1
    if ( away_count >= AWAY_THRESHOLD or disconnect ) and device_present:
        device_present = False
        away_count = 0
        logging.info('Device away. Running ' + AWAY_COMMAND)
        subprocess.run(AWAY_COMMAND, shell=True)

def bluetooth_listen(addr, threshold, here_callback, away_callback, sleep=1, debug=False):
    while True:
        b = BluetoothRSSI(addr=addr)
        rssi = b.get_rssi()
        if debug:
            logging.debug("addr: {}, rssi: {}".format(addr, rssi))
        # Sleep and then skip to next iteration if device not found
        if rssi is None:
            away_callback(True)
            time.sleep(sleep)
            continue
        # Trigger if RSSI value is within threshold
        if rssi < threshold:
            away_callback(False)
        else:
            here_callback()
        # Delay between iterations
        time.sleep(sleep)


def start_thread(addr, here_callback, away_callback, threshold=THRESHOLD, sleep=SLEEP, debug=DEBUG):
    thread = threading.Thread(
        target=bluetooth_listen,
        args=(),
        kwargs={
            'addr': addr,
            'threshold': threshold,
            'here_callback': here_callback,
            'away_callback': away_callback,
            'sleep': sleep,
            'debug': debug
        }
    )
    # Daemonize
    thread.daemon = True
    # Start the thread
    thread.start()
    return thread


def main():
    logging.info("Started btproxipy for device: " + BT_ADDR)
    if not BT_ADDR:
        logging.warning("Please edit this file and set BT_ADDR_LIST variable")
        sys.exit(1)
    threads = []
    th = start_thread(addr=BT_ADDR, here_callback=here_callback, away_callback=away_callback)
    threads.append(th)
    while True:
        # Keep main thread alive
        time.sleep(1)


if __name__ == '__main__':
    main()
