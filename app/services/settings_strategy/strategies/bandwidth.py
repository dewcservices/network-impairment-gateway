import app.services.settings_strategy.isetting_strategy import ISettingStrategy

class Bandwidth(ISettingStrategy):

    def getSettingType() -> str:
        return 'bandwidth'

    def execute(command: str, payload) -> str:
        return f"{command} tbf rate {payload.rate} burst {payload.burst}"
