class IProfileStrategy:

    def getSettingType() -> str:
        raise NotImplementedError

    def execute(interface: str, payload) -> str:
        raise NotImplementedError

    def create(interface: str, payload) -> str:
        raise NotImplementedError

    def update(interface: str, payload) -> str:
        raise NotImplementedError
    
    def remove(interface: str, payload) -> str:
        raise NotImplementedError