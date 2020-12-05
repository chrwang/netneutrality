# DNS Packet Throttler
This application can only run on Linux.

This program is written in Python 3.6.9 and utilizes the NetfilterQueue and scapy libraries. Install the Python dependencies using the following:

```bash
apt-get install build-essential python3-dev libnetfilter-queue-dev
pip3 install NetfilterQueue scapy
```

This application requires sudo rights. To run this program, run `execute.py` using the following:

```bash
sudo python3 execute.py
```
