# DNS Packet Throttler
This application can only run on Linux.

This program is written in Python 3.5.2 and utilizes the NetfilterQueue and scapy libraries. Install the Python dependencies using the following:

```bash
sudo apt install python3-pip git libnfnetlink-dev libnetfilter-queue-dev
sudo pip3 install -U git+https://github.com/kti/python-netfilterqueue
sudo pip3 install scapy
```

This application requires sudo rights. To run this program, run `execute.py` using the following:

```bash
sudo python3 execute.py
```
