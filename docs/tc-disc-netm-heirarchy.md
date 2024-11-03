# impairment gateway qdisc structure

## Netem Defaults
General Rule:
Whenever you use the tc qdisc change command to modify netem settings, any parameter that you don't specify will be reset to its default value.

Default delay: 0ms.
Default jitter: 0ms.
Default packet loss: 0%.
Default duplication: 0%.
Default corruption: 0%.
Default reordering: 0%.

## Basic Structure

### Adding - Bandwidth with network emulation

1. Handle 1 is for the qdisc root
2. class 1:1 is the set htb rate and ceiling
3. handle 10 is for qdisc netem

```sh
tc qdisc add dev {interface} root handle 1: htb default 12
# rate: This is the guaranteed minimum bandwidth that will be provided for the traffic.
# ceil: This is the maximum bandwidth limit that can be used if there is available bandwidth
tc class add dev {interface} parent 1: classid 1:1 htb rate {rate} ceil {ceil}
tc qdisc add dev {interface} parent 1:1 handle 10: netem {netem-option}
```

### Example

```sh
tc qdisc add dev eth0 root handle 1: htb default 12
tc class add dev eth0 parent 1: classid 1:1 htb rate 256kbit ceil 256kbit
tc qdisc add dev eth0 parent 1:1 handle 10: netem delay 500ms 200ms loss 40%
```

### Update

#### Update - Bandwidth

Change the htb rate and ceiling for class 1:1
```sh
tc class change dev eth0 parent 1: classid 1:1 htb rate 512kbit ceil 512kbit
```

#### Update - Netem

update the qdisc netem for htb class 1:1


```sh
tc qdisc change dev eth0 parent 1:1 handle 10: netem delay 300ms loss 20%
```

If i added netem settings
tc qdisc add dev eth0 parent 1:1 handle 10: netem delay 500ms 200ms loss 40%
then changed
tc qdisc change dev eth0 parent 1:1 handle 10: netem delay 300ms
would loss remain at 40% or be set back to 0%




## Uplink/Downlink Bandwidth example

[ref](https://github.com/shynuu/trunks)

```sh
ST_IFACE=enp0s8
GW_IFACE=enp0s9

UP=20mbit
RET=50mbit
DELAY=250ms
OFFSET=100ms

# configure TC
sudo tc qdisc del dev $GW_IFACE root
sudo tc filter del dev $GW_IFACE

# configure rules for TC
sudo tc qdisc add dev $GW_IFACE root handle 1:0 htb default 30
sudo tc class add dev $GW_IFACE parent 1:0 classid 1:1 htb rate $UP
sudo tc qdisc add dev $GW_IFACE parent 1:1 handle 2:0 netem delay $DELAY $OFFSET distribution normal
sudo tc filter add dev $GW_IFACE protocol ip parent 1:0 prio 1 handle 10 fw flowid 1:1
sudo tc -s qdisc ls dev $GW_IFACE
sudo tc -s class ls dev $GW_IFACE
sudo tc -s filter ls dev $GW_IFACE

# =========== Configure rules for forward link ============
# configure TC
sudo tc qdisc del dev $ST_IFACE root
sudo tc filter del dev $ST_IFACE

# configure rules for TC
sudo tc qdisc add dev $ST_IFACE root handle 1:0 htb default 30
sudo tc class add dev $ST_IFACE parent 1:0 classid 1:1 htb rate $RET
sudo tc qdisc add dev $ST_IFACE parent 1:1 handle 2:0 netem delay $DELAY $OFFSET distribution normal
sudo tc filter add dev $ST_IFACE protocol ip parent 1:0 prio 1 handle 20 fw flowid 1:1
sudo tc -s qdisc ls dev $ST_IFACE
sudo tc -s class ls dev $ST_IFACE
sudo tc -s filter ls dev $ST_IFACE
```
```sh
# Apply HTB to the uplink interface with a base rate and max ceiling
sudo tc qdisc add dev $UPLINK_INTERFACE root handle 1: htb default 10
sudo tc class add dev $UPLINK_INTERFACE parent 1: classid 1:10 htb rate 512kbit ceil 1mbit
# Attach netem impairments to the HTB class on the uplink interface
sudo tc qdisc add dev $UPLINK_INTERFACE parent 1:10 handle 10: netem delay 100ms 20ms loss 5% corrupt 1%
# Apply HTB to the downlink interface
sudo tc qdisc add dev $DOWNLINK_INTERFACE root handle 1: htb default 20
sudo tc class add dev $DOWNLINK_INTERFACE parent 1: classid 1:20 htb rate 1mbit ceil 2mbit
# Attach netem impairments to the HTB class on the downlink interface
sudo tc qdisc add dev $DOWNLINK_INTERFACE parent 1:20 handle 20: netem delay 50ms 10ms loss 3% corrupt 0.5%
```