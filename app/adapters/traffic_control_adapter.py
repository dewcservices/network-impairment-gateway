class TrafficControlAdapter:
    @staticmethod
    def create_root_qdisc(interface: str):
        return f"tc qdisc add dev {interface} root handle 1:0 htb default 30"

    @staticmethod
    def create_htb_class(interface: str, rate: str, ceil: str):
        return f"tc class add dev {interface} parent 1:0 classid 1:1 htb rate {rate} ceil {ceil}"

    @staticmethod
    def create_netem_qdisc(
        interface: str,
        delay_time: int,
        delay_jitter: int = 0,
        delay_correlation: int = 0,
        loss_percentage: int = 0,
        loss_interval: int = 0,
        loss_correlation: int = 0,
        corrupt_percentage: int = 0,
        corrupt_correlation: int = 0,
    ):
        return f"tc qdisc add dev {interface} parent 1:1 handle 2:0 netem delay {delay_time}ms {delay_jitter}ms {delay_correlation}% loss {loss_percentage}% {loss_correlation}% corrupt {corrupt_percentage}% {corrupt_correlation}%"

    @staticmethod
    def create_filter(
        interface: str,
    ):

        return f"tc filter add dev {interface} protocol ip parent 1:0 prio 1 handle 10 fw flowid 1:1"

    @staticmethod
    def add_percentage(bearer_percentage: int, environment_percentage: int) -> int:
        temp = TrafficControlAdapter.add(bearer_percentage, environment_percentage)
        if temp > 100:
            return 100
        elif temp < 0:
            return 0

        return temp

    @staticmethod
    def add(bearer_value: int, environment_value: int) -> int:
        temp = bearer_value + environment_value
        if temp > 100:
            return 100
        elif temp < 0:
            return 0

        return temp

    @staticmethod
    def update_hbt(interface: str, class_id: str, rate: str, ceil: str) -> str:
        return f"tc class change dev {interface} parent 1:0 classid 1:1 htb rate {rate} ceil {ceil}"

    @staticmethod
    def update_netem(
        interface: str,
        class_id: str,
        handle: str,
        delay_time: int,
        delay_jitter: int = 0,
        delay_correlation: int = 0,
        loss_percentage: int = 0,
        loss_interval: int = 0,
        loss_correlation: int = 0,
        corrupt_percentage: int = 0,
        corrupt_correlation: int = 0,
    ) -> str:
        return f"tc qdisc change dev {interface} parent 1:1 handle 2:0 netem delay {delay_time}ms {delay_jitter}ms {delay_correlation}% loss {loss_percentage}% {loss_correlation}% corrupt {corrupt_percentage}% {corrupt_correlation}%"

    @staticmethod
    def clear_qdisc(interface: str):
        return f"tc qdisc del dev {interface} root"

    @staticmethod
    def clear_filter(interface: str):
        return f"tc filter del dev {interface}"
