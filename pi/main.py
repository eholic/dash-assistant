import queue
import threading
import time
import logging
import logging.config
import yaml
from scapy.all import sniff
from google_assist import gassist
from config import Config

# Ref: https://github.com/Nekmo/amazon-dash/blob/develop/amazon_dash/discovery.py

# Amazon Dash Mac Devices. Source: https://standards.ieee.org/develop/regauth/oui/oui.csv
AMAZON_DEVICES = [
    'F0:D2:F1',
    '88:71:E5',
    'FC:A1:83',
    'F0:27:2D',
    '74:C2:46',
    '68:37:E9',
    '78:E1:03',
    '38:F7:3D',
    '50:DC:E7',
    'A0:02:DC',
    '0C:47:C9',
    '74:75:48',
    'AC:63:BE',
    'FC:A6:67',
    '18:74:2E',
    '00:FC:8B',
    'FC:65:DE',
    '6C:56:97',
    '44:65:0D',
    '50:F5:DA',
    '68:54:FD',
    '40:B4:CD',
    '00:71:47',
    '4C:EF:C0',
    '84:D6:D0',
    '34:D2:70',
    'B4:7C:9C',
    'F0:81:73',
]

def is_amazon_dev(pkt):
    return pkt.src.upper()[:8] in AMAZON_DEVICES


def press_to_assist(q):
    last_press = None
    last_mac = None
    while True:
        mac = q.get().upper()
        if last_mac == mac and time.time() - last_press < 1: # ignore multi messages within short time
            continue
        logging.info(mac + 'is pressed.')
        if mac in Config.actions.keys():
            gassist(Config.actions[mac])
        last_press = time.time()
        last_mac = mac


if __name__ == '__main__':
    # Setup logging.
    with open('logging.yml', 'r') as f:
        log_yml = yaml.safe_load(f.read())
    logging.config.dictConfig(log_yml)
    #  logging.basicConfig(level=logging.INFO)

    q = queue.Queue()
    threading.Thread(target=press_to_assist, daemon=True, args=(q, )).start()

    try:
        print('Ready to press Amazon Dash Button')
        # doc: https://scapy.readthedocs.io/en/latest/api/scapy.sendrecv.html#scapy.sendrecv.sniff
        sniff(filter="arp or (udp and src port 68 and dst port 67 and src host 0.0.0.0)",
              prn=lambda pkt: q.put(pkt.src),
              store=False,
              lfilter=lambda p: is_amazon_dev(p),
              )

    except PermissionError:
        logging.error('Please run by sudo', exc_info=True)
