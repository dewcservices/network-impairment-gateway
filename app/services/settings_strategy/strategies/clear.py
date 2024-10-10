import app.services.settings_strategy.isetting_strategy import ISettingStrategy

class Clear(ISettingStrategy):

    def getSettingType() -> str:
        return 'clear'

    def execute(command: str, payload) -> str:
        return f"{command}"
