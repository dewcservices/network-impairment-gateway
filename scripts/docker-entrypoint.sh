#!/bin/bash

# Enable IP forwarding to allow traffic to pass through the gateway
sysctl -w net.ipv4.ip_forward=1

# Set up iptables rules to forward traffic between eth0 (network_a) and eth1 (network_b)
iptables -A FORWARD -i eth0 -o eth1 -j ACCEPT
iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT

# Enable NAT for outgoing packets from eth0 to eth1 and vice versa (optional, for proper routing)
iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# Impair all traffic passing through as eth0 is passing to eth1
tc qdisc add dev eth0 root netem delay 100ms loss 10%

# Start fastapi app with uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port 8000