import app.services.profile_strategy.iprofile_strategy import IProfileStrategy

class FourG(IProfileStrategy):

    """
    4G LTE Profile
    4G LTE offers higher speeds and lower latency than satellite connections, 
    but the performance can degrade with congestion, signal strength, and mobility 
    (e.g., moving between towers). Typical bandwidth can vary from 10 Mbps to 50 Mbps downlink, 
    depending on signal strength and network load.
    -----------------------------------
    Bandwidth: 10 Mbps (downlink), 2 Mbps (uplink).
    Latency: 50ms (generally low but can spike during congestion).
    Jitter: 30ms (due to network congestion or tower handoffs).
    Packet Loss: 1% (may occur under high network load or weak signals).
    """

    def getSettingType() -> str:
        raise '4g'

    def execute(interface: str, payload) -> str:
        return  f"sudo tc qdisc add dev {interface} root handle 1: htb default 12 && " \
                f"sudo tc class add dev {interface} parent 1: classid 1:1 htb rate 2mbit ceil 10mbit && " \
                f"sudo tc qdisc add dev {interface} parent 1:1 handle 10: netem delay 50ms 30ms loss 1%"