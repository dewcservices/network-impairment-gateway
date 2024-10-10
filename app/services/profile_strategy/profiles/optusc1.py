import app.services.profile_strategy.iprofile_strategy import IProfileStrategy

class OptusC1(IProfileStrategy):

    """
    Optus C1 Profile
    Optus C1 is a geostationary satellite providing communications across Australia, Southeast Asia, and parts of the Pacific. It is commonly used for defense and commercial communications. Latency is higher due to its geostationary orbit (approximately 35,786 km), and the bandwidth is more constrained compared to Starlink.
    -----------------------------------
    Bandwidth: 2 Mbps (uplink), 5 Mbps (downlink)
    Latency: 600ms (typical for geostationary satellites)
    Jitter: 50ms (due to signal fluctuations)
    Packet Loss: 5% (can occur during atmospheric conditions or in high-demand situations)
    """

    def getSettingType() -> str:
        raise 'optus-c1'

    def execute(interface: str, payload) -> str:
        return  f"sudo tc qdisc add dev {interface} root handle 1: htb default 12 && " \
                f"sudo tc class add dev {interface} parent 1: classid 1:1 htb rate 2mbit ceil 5mbit && " \
                f"sudo tc qdisc add dev {interface} parent 1:1 handle 10: netem delay 600ms 50ms loss 5%"