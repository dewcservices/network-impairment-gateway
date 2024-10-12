from app.services.settings_strategy.isetting_strategy import ISettingStrategy


class PacketLoss(ISettingStrategy):

    def getSettingType() -> str:
        return "packet-loss"

    def execute(interface: str, command: str, payload) -> str:
        return f"{command} netem loss {payload.loss}"
