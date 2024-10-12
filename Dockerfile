# Dockerfile for the impairment gateway container
FROM oraclelinux:8

# Install iptables and tc
RUN yum update -y && yum install -y iproute iproute-tc iptables

# Set up your entrypoint script to configure tc and iptables
COPY --chmod=0755 scripts/docker-entrypoint.sh /usr/local/bin/

# Set the entrypoint to the script
ENTRYPOINT ["docker-entrypoint.sh"]