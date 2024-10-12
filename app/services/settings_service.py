import subprocess
from app.services.interfaces.isetting_service import ISettingService
from app.services.settings_strategy.setting_context import SettingsContext

class SettingsService(ISettingService):

    def __init__(self, interface: str):
        self.interface = interface
        self.strategies = SettingsContext() 

    # Function to apply tc settings
    def _apply_tc(command: str):
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout, result.stderr

    def change(self, setting_type: str, payload):
        action = "change"
        command = f"tc qdisc {action} dev {self.interface} root"
       return _apply_tc(self.strategies.get(setting_type).execute(command, payload))

    def add(self, setting_type: str, payload):
        action = "add"
        command = f"tc qdisc {action} dev {self.interface} root"
        return _apply_tc(self.strategies.get(setting_type).execute(command, payload))

    def clear(self, setting_type: str):
        action = "del"
        command = f"tc qdisc {action} dev {self.interface} root"
        return _apply_tc(self.strategies.get(setting_type).execute(command, {}))
