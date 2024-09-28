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

#### Step 1 - Enable the System-Wide Podman Socket

```sh
sudo systemctl enable --now podman.socket 
```

#### Step 2 - Local user confirms podman socker is working
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

#### Softchage

exec into the impairment_gateway container and modify the tc settings in the terminal

```
docker exec -it impairment_gateway sh
# 
```

#### Hard change
Modify tc settings in ./scripts/docker-entrypoint.sh, bring down the example, and redeploy

```
docker-compose -f docker-compose.yaml down
```