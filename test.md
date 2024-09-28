# Test 1 - Ping Test

## settings
tc qdisc add dev eth0 root netem delay 1000ms loss 50%
tc qdisc add dev eth1 root netem delay 1000ms loss 50%

## Results

### A -> B Ping
/ # ping -c 3 172.19.0.2
PING 172.19.0.2 (172.19.0.2): 56 data bytes
64 bytes from 172.19.0.2: seq=3 ttl=63 time=2040.518 ms
64 bytes from 172.19.0.2: seq=5 ttl=63 time=2000.224 ms
64 bytes from 172.19.0.2: seq=11 ttl=63 time=2000.185 ms

### B -> A Ping
/ # ping -c 3 172.18.0.2
PING 172.18.0.2 (172.18.0.2): 56 data bytes
64 bytes from 172.18.0.2: seq=0 ttl=63 time=2000.249 ms
64 bytes from 172.18.0.2: seq=1 ttl=63 time=2000.192 ms

--- 172.18.0.2 ping statistics ---
3 packets transmitted, 2 packets received, 33% packet loss
round-trip min/avg/max = 2000.192/2000.220/2000.249 ms

# Test 2 - Ping Test
## settings
tc qdisc add dev eth0 root netem delay 1000ms loss 50%

## Results
### A -> B Ping
/ # ping -c 3 172.19.0.2
PING 172.19.0.2 (172.19.0.2): 56 data bytes
64 bytes from 172.19.0.2: seq=1 ttl=63 time=1000.184 ms

--- 172.19.0.2 ping statistics ---
3 packets transmitted, 1 packets received, 66% packet loss
round-trip min/avg/max = 1000.184/1000.184/1000.184 ms

### B -> A Ping
/ # ping -c 5 172.18.0.2
PING 172.18.0.2 (172.18.0.2): 56 data bytes
64 bytes from 172.18.0.2: seq=1 ttl=63 time=1000.183 ms
64 bytes from 172.18.0.2: seq=2 ttl=63 time=1000.111 ms

--- 172.18.0.2 ping statistics ---
5 packets transmitted, 2 packets received, 60% packet loss
round-trip min/avg/max = 1000.111/1000.147/1000.183 ms