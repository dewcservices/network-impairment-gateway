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

```sh
# Add root qdisc to eth0
tc qdisc add dev eth0 root handle 1: htb default 12
# Create uplink class (2 Mbps)
tc class add dev eth0 parent 1: classid 1:1 htb rate 2mbit ceil 2mbit
# Create downlink class (5 Mbps)
tc class add dev eth0 parent 1: classid 1:2 htb rate 5mbit ceil 5mbit
# Filter for uplink traffic
tc filter add dev eth0 protocol ip parent 1: prio 1 u32 match ip src 192.168.1.100/32 flowid 1:1
# Filter for downlink traffic
tc filter add dev eth0 protocol ip parent 1: prio 1 u32 match ip dst 192.168.1.100/32 flowid 1:2
# Apply netem for uplink traffic (100ms delay, 10% loss)
tc qdisc add dev eth0 parent 1:1 handle 10: netem delay 100ms loss 10%
# Apply netem for downlink traffic (50ms delay, 5% loss)
tc qdisc add dev eth0 parent 1:2 handle 20: netem delay 50ms loss 5%
```