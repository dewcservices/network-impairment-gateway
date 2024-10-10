# network-impairment-gateway
Linux based network impairment gateway


[Ref](https://blogs.oracle.com/cloud-infrastructure/post/linux-traffic-controller-latency-fetch-size-db)

## Infrastructure

### Local User Permissions

Prior to being able to run/test the impairment gateway the local user will require priviledged access to the following:

| Command   | Description                                                              | Typical Filepath          | Purpose  |
|-----------|--------------------------------------------------------------------------|---------------------------|----------|
| iptables  | Manages IPv4 and IPv6 packet filtering and NAT rules (firewall utility). | `/usr/sbin/iptables`      | Provides the impairment gateway with the ability to pass traffic from eth0 to/from eth1 |
| ip        | Utility to show/manipulate routing, devices, policy routing, and tunnels | `/usr/sbin/ip`            | used to set/change the default subnet gateways on test nodes |
| ifconfig  | Configures network interfaces (obsolete, replaced by `ip` on modern distros). | `/sbin/ifconfig`     | available to view interfaces |
| tc        | Configures network traffic control, including queueing disciplines like `netem`. | `/usr/sbin/tc`    | Provides the impairment capability to the network impairment gateway |


```sh
sudo groupadd developers
sudo usermod -aG developers <username>
sudo vim /etc/sudoers

--------VIM: Add Developer to sudoers for the required applications

%developers ALL=(ALL) NOPASSWD: /usr/sbin/iptables, /usr/sbin/tc, /usr/sbin/ip, /usr/sbin/ifconfig

--------
```

### Ensuring Network Emulation is installed

When testing the impairment gateway with Oracle Linux 8 netem was not available which is required by tc.


### Test if netem is available

check if the sch_netem module is available:

```sh
#lsmod | grep sch_netem
sch_netem              xyzxy  1
```

If the module isn't already loaded, try loading manually:

```sh
sudo modprobe sch_netem
```

If this fails you are missing netem and it needs to be installed

### Installing netem on Oracle Linux
[Ref](https://community.oracle.com/mosc/discussion/4565567/quesition-about-linux-traffic-control-tc-on-linux-8-9-and-9-4)
#### Step 1 - Determine your kernel version

```sh
uname -r
```

5.15.0-300.161.13.el8uek.x86_64
5.15.0-300.161.13.el8rhck.x86_64

#### Step 2 - install netem

For Red Hat Compatible Kernel (RHCK) module sch_netem is available from:

```sh
sudo yum install kernel-modules-extra.
```

For Unbreakable Enterprise Kernel UEK (Oracle), however, module sch_netem is available from:
```
sudo yum install kernel-uek-modules-extra
```

#### Step 3 - Reboot

```
sudo reboot
```

#### Step 4 - Verify netem installation

After rebooting, check if the sch_netem module is now available:

```sh
lsmod | grep sch_netem
```

If the module isn't already loaded, you can manually load it:

```sh
sudo modprobe sch_netem
```

### Configuring Docker Compose on Oracle Linux 

[reference](https://docs.oracle.com/en/learn/ol-podman-compose/index.html#confirm-docker-compose-is-working)

#### Step 1 - Enable Podman Socket rootless for the current user
```sh
systemctl --user enable podman.socket
systemctl --user start podman.socket
```

You can add to .bash_profile for convinence

#### Step 2 - Local user confirms podman socket is working
```sh
podman info | grep -i remotesocket -A2
curl -w "\n" -H "Content-Type: application/json" --unix-socket /run/user/$UID/podman/podman.sock http://localhost/_ping
```

#### Step 3 - Added Environement Variable for Docker compose

```sh
export DOCKER_HOST=unix:///run/user/$UID/podman/podman.sock # Set environment variable for the location of the Podman socket.
export DOCKER_BUILDKIT=0 # new buildkit doesn't work with podman
```

Todo 
- Enable the System-Wide Podman Socket on start up
- DOCKER_HOST needs to be set in every users bash_profile

## Running the Example

### Confirming impairment settings

exec into the impairment_gateway container and modify the tc settings in the terminal

```
docker exec -it impairment_gateway sh
# tc qdisc show dev eth0
qdisc netem 8001: root refcnt 5 limit 1000 delay 100ms loss 10%
```

### Run the example

```
docker-compose -f docker-compose.yaml up -d --build --force-recreate
```

### Ping test

```
docker exec -it container_a sh
# ping -c 3 172.19.0.2
```

```
docker exec -it container_b sh
# ping -c 3 172.18.0.2
```

### Test impairment

#### Softchange

exec into the impairment_gateway container and modify the tc settings in the terminal

```
docker exec -it impairment_gateway sh
# tc qdisc change dev eth0 root netem loss 50%
# tc qdisc change dev eth0 root netem delay 10m
```

#### Hard change
Modify tc settings in ./scripts/docker-entrypoint.sh, bring down the example, and redeploy

```
docker-compose -f docker-compose.yaml down
```

### complex impairments

```sh
# 1. Delete existing qdisc
tc qdisc del dev eth0 root

# 2. Add HTB qdisc to control bandwidth
tc qdisc add dev eth0 root handle 1: htb default 12

# 3. Create an HTB class with a 5Mbps limit
tc class add dev eth0 parent 1: classid 1:1 htb rate 2mbit ceil 2mbit

# 4. Add netem qdisc to simulate delay and packet loss
tc qdisc add dev eth0 parent 1:1 handle 10: netem delay 100ms loss 10%

# 5. (Optional) Add a filter for specific traffic (e.g., all traffic)
tc filter add dev eth0 protocol ip parent 1:0 prio 1 u32 match ip src 0.0.0.0/0 flowid 1:1

# 6. Verify settings
tc -s qdisc show dev eth0
tc class show dev eth0
```

#### Changing Bandwidth

```sh
# 1. Check the current settings: To check the current tc settings and see which class is handling the bandwidth restriction, use:
tc class show dev eth0
#> class htb 1:1 root rate 5Mbit ceil 5Mbit

# 2. Change the bandwidth limit: To reduce the bandwidth, you can use the tc class change command to modify the existing class. For example, to reduce the bandwidth from 5 Mbps to 2 Mbps, you would run:

tc class change dev eth0 parent 1: classid 1:1 htb rate 2mbit ceil 2mbit

# - parent 1: refers to the HTB qdisc.
# - classid 1:1 refers to the class ID you want to change.
# - rate 2mbit limits the bandwidth to 2 Mbps.
# - ceil 2mbit sets the maximum bandwidth ceiling to 2 Mbps.
```

#### Change Latency and Packet Loss

```sh
# 1. Check current netem settings: To see if there are any existing netem rules applied, run

tc qdisc show dev eth0
#> qdisc netem 10: parent 1:1 limit 1000 delay 100ms loss 10%

# 2. Change the existing netem qdisc: To modify the latency and packet loss settings, use the tc qdisc change command.

# change just the latency
tc qdisc change dev eth0 parent 1:1 handle 10: netem delay 200ms

# change just the packet loss
sudo tc qdisc change dev eth0 parent 1:1 handle 10: netem loss 5%

# change both
sudo tc qdisc change dev eth0 parent 1:1 handle 10: netem delay 200ms loss 5%
```

#### Simulating Communications Bearers

##### Bandwidth
##### Latency
##### Jitter (Variable Latency) 
Satellite communications often have fluctuating delays due to varying conditions in the atmosphere or network routing. Jitter can be simulated using tc netem by introducing variable delay:

latency 500ms +-100ms
```sh
tc qdisc add dev eth0 root netem delay 500ms 100ms
```

##### Packet Reordering
Packet reordering occurs frequently in satellite and DDIL networks, especially when multiple paths are involved. netem allows you to simulate out-of-order packets.

```sh
tc qdisc change dev eth0 root netem reorder 25% 50%
```
    - reorder 25%: Specifies that 25% of packets will be delivered out of order.
    - 50%: The correlation percentage, which means that once reordering starts, it will continue with a 50% probability.

##### Corruption (Bit Errors in Packets)
Satellite and DDIL networks can suffer from bit errors due to noise, interference, or weak signals, which can cause packets to be corrupted. You can simulate this with:

```sh
tc qdisc change dev eth0 root netem corrupt 1%
```

##### Intermittent Connectivity (Dropping connections)
DDIL environments often involve intermittent connectivity where the link is temporarily dropped. You can simulate this by periodically introducing packet loss (complete disconnections) using tc.

```sh
tc qdisc change dev eth0 root netem loss 100% 500ms
```

This configuration introduces a 100% packet loss (disconnection) for 500ms intervals, simulating brief disconnections

##### Delay Variation with Correlation

If you want to introduce delay variations that are not completely random but correlated over time (which is often the case in satellite communications), you can use the delay with correlation:

```sh
tc qdisc change dev eth0 root netem delay 500ms 50ms 25%
# delay 500ms 50ms: Adds a base delay of 500ms with a random variation of ±50ms.
# 25%: The correlation, meaning consecutive packets have a 25% chance of having similar delays.
```

##### Simulating Link Asymmetry (Different rates for upload/download)
Many satellite links have asymmetric bandwidth where download and upload speeds differ. You can simulate this by applying different rate limits on different interfaces (e.g., one interface for upload, one for download).

```sh
tc qdisc add dev eth0 root tbf rate 512kbit burst 16kbit latency 100ms
tc qdisc add dev eth1 root tbf rate 2mbit burst 32kbit latency 100ms
```

#### Enable the System-Wide Podman Socket
- Doesn't work as is starts /run/podman/podman.sock.
```sh
sudo systemctl enable --now podman.socket 
```