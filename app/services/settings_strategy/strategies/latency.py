import app.services.settings_strategy.isetting_strategy import ISettingStrategy

class Latency(ISettingStrategy):

    def getSettingType() -> str:
        return 'latency'

    def execute(command: str, payload) -> str:
        return f"{command} netem delay {payload.delay}"