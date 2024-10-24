import ipaddress

from app.exception.request_processing_exception import RequestProcessingException


class TrafficControlAdapter:
    @staticmethod
    def create_root_qdisc(self, interface: str):
        return f"tc qdisc add dev {self.interface} root handle 1: htb default 12"

    @staticmethod
    def create_htb_class(self, interface: str, rate: str, ceil: str, class_id: str):
        return f"tc class add dev {interface} parent 1: classid {class_id} htb rate {rate} ceil {ceil}"

    @staticmethod
    def create_netem_qdisc(
        self,
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
    ):
        return f"tc qdisc add dev {interface} parent {class_id} handle {handle} netem delay {delay_time}ms {delay_jitter}ms {delay_correlation}% loss {loss_percentage}% {loss_interval}ms {loss_correlation}% corrupt {corrupt_percentage}% {corrupt_correlation}%"

    @staticmethod
    def create_filter(
        self,
        interface: str,
        direction: str,
        ip_addr: str,
        flow_id: str,
    ):
        if direction not in ["src", "dst"]:
            raise RequestProcessingException(
                status_code=400, detail="Direction must be either 'src' or 'dst'."
            )

        try:
            ip_addr = ipaddress.IPv4Address(ip_addr)  # Invalid IP
        except ipaddress.AddressValueError as e:
            raise RequestProcessingException(
                status_code=400, detail=f"Invalid IPv4 address: {e}"
            )

        return f"tc filter add dev {interface} protocol ip parent 1: prio 1 u32 match ip {direction} {ip_addr} flowid {flow_id}"

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
    def update_hbt(self, interface: str, class_id: str, rate: str, ceil: str) -> str:
        return f"tc class change dev {interface} parent 1: classid {class_id} htb rate {rate} ceil {ceil}"

    @staticmethod
    def update_netem(
        self,
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
        return f"tc qdisc change dev {interface} parent {class_id} handle {handle} netem delay {delay_time}ms {delay_jitter}ms {delay_correlation}% loss {loss_percentage}% {loss_interval}ms {loss_correlation}% corrupt {corrupt_percentage}% {corrupt_correlation}%"
