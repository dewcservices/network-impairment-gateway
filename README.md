# Network Impairment Gateway

The Network Impairment Gateway is a rest-api service designed to simulate DDIL (Disrupted, Disconnected, Intermittent, Limited) network conditions in edge-to-cloud environments. This service complements the [Network Impairment Gateway UI](https://github.com/dewcservices/network-impairment-gateway-ui). It utilizes two network interfaces and applies traffic impairments (e.g., latency, packet loss, and corruption) via iptables, tc, and netem. This setup allows for simulating diverse communication bearers such as satellite, 4G, and broadband, as well as testing applications under varied network conditions.

## Features

- Traffic Impairment: Configurable impairments, including delay, packet loss, and corruption.
- DDIL Support: Emulates challenging network conditions in edge-to-cloud scenarios.
- Uplink/Downlink Mode: Applies impairments on separate paths for uplink and downlink.

# Requirements

## References

A. [Ref](https://blogs.oracle.com/cloud-infrastructure/post/linux-traffic-controller-latency-fetch-size-db)

## Operating System

### General Requirements
- Linux OS
    - Has only been tested on Oracle Linux 8

### Installing netem on Oracle Linux

[Ref](https://community.oracle.com/mosc/discussion/4565567/quesition-about-linux-traffic-control-tc-on-linux-8-9-and-9-4)

#### Step 1 - Determine your kernel version

```sh
uname -r
> 5.15.0-300.161.13.el8uek.x86_64 # example response for oracle linux unbreakable kernel
> 5.15.0-300.161.13.el8rhck.x86_64 # example response for redhat compatible kernel
```

#### Step 2 - Install netem

This step will require root priveledges and is best implement via cloud-init or ansible

#### Red Hat Compatible Kernel (RHCK)

For Red Hat Compatible Kernel (RHCK) module sch_netem is available from:

```sh
sudo yum install kernel-modules-extra.
```
#### Unbreakable Enterprise Kernel UEK

For Unbreakable Enterprise Kernel UEK (Oracle), however, module sch_netem is available from:

```sh
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

### Local User Permissions

Prior to being able to run/test the impairment gateway the local user will require priviledged access to the following:

| Command   | Description                                                              | Typical Filepath          | Purpose  |
|-----------|--------------------------------------------------------------------------|---------------------------|----------|
| iptables  | Manages IPv4 and IPv6 packet filtering and NAT rules (firewall utility). | `/usr/sbin/iptables`      | Provides the impairment gateway with the ability to pass traffic from eth0 to/from eth1 |
| ip        | Utility to show/manipulate routing, devices, policy routing, and tunnels | `/usr/sbin/ip`            | used to set/change the default subnet gateways on test nodes |
| ifconfig  | Configures network interfaces (obsolete, replaced by `ip` on modern distros). | `/sbin/ifconfig`     | available to view interfaces |
| tc        | Configures network traffic control, including queueing disciplines like `netem`. | `/usr/sbin/tc`    | Provides the impairment capability to the network impairment gateway |
| | `/sbin/`| |
| modprobe | Loads kernel modules, such as sch_netem, which enables network emulation capabilities in tc. | `/sbin/modprobe  sch_netem` | Used to load the sch_netem module, enabling tc to perform network impairment functions like delay, loss, and corruption. |

#### Creating a Group with Required Permissions

```sh
sudo groupadd developers
sudo usermod -aG developers <username>
sudo vim /etc/sudoers.d/developers
```

/etc/sudoers.d/developers
```sh
%developers ALL=(ALL) NOPASSWD: /usr/sbin/iptables, /usr/sbin/tc, /usr/sbin/ip, /usr/sbin/ifconfig, /sbin/modprobe  sch_netem
```

# Installation

## Local Testing in Docker/Podman

### Install docker compose

### Configuring Docker Compose on Oracle Linux 

```sh
sudo curl -SL https://github.com/docker/compose/releases/download/v2.15.1/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

### Enable podman
[reference](https://docs.oracle.com/en/learn/ol-podman-compose/index.html#confirm-docker-compose-is-working)

```sh
sudo systemctl enable --now podman.socket
```

#### Step 1 - Enable Podman Socket rootless for the current user

```sh
systemctl --user enable podman.socket
systemctl --user start podman.socket
```

#### Step 2 - Added Environment Variable for Docker compose

```sh
vim /etc/profile.d/podman.sh
```

/etc/profile.d/podman.sh
```sh
# Set environment variable for the location of the Podman socket
export DOCKER_HOST=unix:///run/user/$UID/podman/podman.sock
# Disable BuildKit as it doesn't work well with Podman
export DOCKER_BUILDKIT=0
```

```sh
chmod 0644 /etc/profile.d/podman.sh
```

#### Step 3 - Local user confirms podman socket is working
```sh
podman info | grep -i remotesocket -A2
curl -w "\n" -H "Content-Type: application/json" --unix-socket /run/user/$UID/podman/podman.sock http://localhost/_ping
```

### Running the Example

```sh
git clone https://github.com/yourusername/network-impairment-gateway.git
cd network-impairment-gateway
docker-compose -f docker-compose.yaml up -d
```

Using vscode port forward port 8000 and you should be able to access swagger at [http://localhost:8000/docs](http://localhost:8000/docs)

#### Ping test

```
docker exec -it container_a sh
# ping -c 3 172.19.0.2
```

```
docker exec -it container_b sh
# ping -c 3 172.18.0.2
```

### Test impairment

#### Setting Impairment

```
POST /api/set-impairment
- payload: { 'bearer_id': int, 'environment_id': int }
```











