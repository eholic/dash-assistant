import queue
import threading
import time
import logging
import logging.config
import yaml
from google_assist import gassist
from amazon_dash import dash_sniff
from config import Config


def press_to_assist(q):
    last_press = None
    last_mac = None
    while True:
        mac = q.get().upper()
        if last_mac == mac and time.time() - last_press < 1: # ignore multi messages within short time
            continue
        logging.info(mac + ' is pressed.')
        if mac in Config.actions.keys():
            gassist(Config.actions[mac])
        last_press = time.time()
        last_mac = mac


if __name__ == '__main__':
    # Setup logging.
    with open('logging.yml', 'r') as f:
        log_yml = yaml.safe_load(f.read())
    logging.config.dictConfig(log_yml)

    q = queue.Queue()
    threading.Thread(target=press_to_assist, daemon=True, args=(q, )).start()

    dash_sniff(lambda pkt: q.put(pkt.src))
