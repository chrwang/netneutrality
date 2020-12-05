# Imports
from netfilterqueue import NetfilterQueue
from scapy.all import *
import os
import csv
import logging
import argparse
import time
from functools import partial

parser = argparse.ArgumentParser(description='DNS block.')
parser.add_argument("filepath", help="path to blocklist file")
parser.add_argument("-v", help="verbose", action="store_true")

# Define iptables rule to bind to. Change the queue number to something unique.
QUEUE_NUM = 1
RULE = "OUTPUT -p udp --dport 53 -j NFQUEUE --queue-num " + str(QUEUE_NUM)


def load_rules(fname):
    """
    Load block rules from a file.
    Arguments:
        fname: the file path to load from.
    """
    result = {}
    with open(fname, newline="") as rulefile:
        reader = csv.DictReader(rulefile)
        for r in reader:
            result[r["url"]] = {
                "type": r["type"], 
                "dest": r["dest"],
                "delay": int(r["delay"]) if r["delay"] else 0
            }
    return result


def rule_in(rdict, url):
    """
    Check if a url is in the rules specified by the dictionary.
    Arguments:
        rdict: the dictionary to check in.
        url: the url to check.
    """
    for k in rdict.keys():
        if k in url:
            return rdict[k]
    return None


def process(rdict, packet):
    """
    Process a packet.
    Arguments:
        rdict: the rules dict to process packets by.
        packet: the packet object to process.
    """
    logging.info(f"Recieved packet {packet}")
    # Get the packet payload from nfqueue
    data = packet.get_payload()
    # Convert it into a scapy packet instance
    pkt = IP(data)
    # Check if it contains a DNS query. If not, pass it on.
    if not pkt.haslayer(DNSQR):
        packet.accept()
    else:
        # If it does, check if the requested domain contains a domain to rewrite
        name = str(pkt[DNS].qd.qname)
        d = rule_in(rdict, name)
        if d is not None:
            if d["type"] == "BLOC":
                logging.info(f"Blocking outgoing packet to {name}")
                rcod = 3
                ac = 0
                answ = None
            elif d["type"] == "RDIR":
                logging.info(f"Redirecting outgoing packet to {name} to {d['dest']}")
                rcod = 0
                ac = 1
                answ = DNSRR(type="A", rrname=pkt[DNS].qd.qname, rdata=d["dest"])
            elif d["type"] == "THR":
                logging.info(f"Throttling outgoing packet to {name} by {d['delay']} ms")
                time.sleep(d["delay"] / 1000)
                packet.accept()
                return
            else:
                logging.info(f"Accepting packet to {name} normally")
                packet.accept()
                return
            # Build a new packet with the rewritten data
            spoofed_pkt = IP(dst=pkt[IP].src, src=pkt[IP].dst)/\
                             UDP(dport=pkt[UDP].sport, sport=pkt[UDP].dport)/\
                             DNS(id=pkt[DNS].id, qr=1, ra=1, aa=1, rcode=rcod,qd=pkt[DNS].qd, ancount=ac, an=answ)
            # Set the payload of the queued packet to the new payload
            packet.set_payload(raw(spoofed_pkt))
        # Pass the packet back to iptables
        packet.accept()


def main(fname):
    ruledict = load_rules(fname)
    # Instantiate a queue.
    queue = NetfilterQueue()
    # Bind to the same queue number used in the rule.
    queue.bind(QUEUE_NUM, partial(process, ruledict))
    try:
        os.system("iptables -t nat -A " + RULE)
        logging.info("Bound using rule " + RULE)
        logging.info("Starting queue...")
        # Blocks until error or stop.
        queue.run()
        logging.info("Exiting...")
    except BaseException as e:
        logging.info("Encountered an error, exiting...")
        os.system("iptables -t nat -D " + RULE)
        queue.unbind()
        exit(1)

if __name__ == "__main__":
    args = parser.parse_args()
    if (args.v):
        logging.basicConfig(level=logging.INFO)
    main(args.filepath)
