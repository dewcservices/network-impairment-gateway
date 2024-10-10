import app.services.profile_strategy.iprofile_strategy import IProfileStrategy

class ConsumerSatellite(IProfileStrategy):

    """
    Consumer Satellite Profile
    Consumer satellite connections, such as those provided by HughesNet or Viasat, generally have higher latency than 
    terrestrial connections due to geostationary orbit, and bandwidth is often shared among users, leading to lower speeds during peak times.    
    -----------------------------------
    Bandwidth: 25 Mbps (downlink), 3 Mbps (uplink) — typical for consumer satellite plans.
    Latency: 600ms (due to geostationary orbit).
    Jitter: 50ms (due to network congestion and signal variation).
    Packet Loss: 3% (common in consumer satellite services due to shared bandwidth and interference).
    """

    def getSettingType() -> str:
        raise 'consumer-sat'

    def execute(interface: str, payload) -> str:
        return  f"sudo tc qdisc add dev {interface} root handle 1: htb default 12 && " \
                f"sudo tc class add dev {interface} parent 1: classid 1:1 htb rate 3mbit ceil 25mbit && " \
                f"sudo tc qdisc add dev {interface} parent 1:1 handle 10: netem delay 600ms 50ms loss 3%"