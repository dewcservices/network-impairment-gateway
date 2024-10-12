from app.services.interfaces.isetting_service import ISettingService


class SettingService(ISettingService):

    def __init__(self, interface: str):
        self.interface = interface

    def create_htb_netem_qdiscs(self, payload):
        return "htb and netem qdisc added"

    def update_htb(self, payload):
        return "bandwidth updated"

    def update_netem(self, payload):
        return "netem updated"

    def delete_htb_netem_qdiscs(self):
        return "htb and netem qdisc added"
