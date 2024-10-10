class ISettingStrategy:

    def getSettingType() -> str:
        raise NotImplementedError

    def execute(command: str, payload) -> str:
        raise NotImplementedError
