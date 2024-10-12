from app.services.profile_strategy.iprofile_strategy import IProfileStrategy


class Starlink(IProfileStrategy):
    """
    Starlink Profile
    Starlink is a low-earth orbit (LEO) satellite network that generally offers low latency and high bandwidth compared to traditional
    geostationary satellite networks. The bandwidth can range from 50 Mbps to 200 Mbps, and the latency is typically between 20ms to 40ms.
    -----------------------------------
    Bandwidth: 100 Mbps (typical)
    Latency: 30ms
    Jitter: 10ms (due to LEO handoffs and atmospheric conditions)
    Packet Loss: 1% (may occur occasionally during handoffs)
    """

    def getSettingType() -> str:
        raise "optus-c1"

    def execute(interface: str, payload) -> str:
        return (
            f"sudo tc qdisc add dev {interface} root handle 1: htb default 12 && "
            f"sudo tc class add dev {interface} parent 1: classid 1:1 htb rate 100mbit ceil 100mbit && "
            f"sudo tc qdisc add dev {interface} parent 1:1 handle 10: netem delay 30ms 10ms loss 1%"
        )
