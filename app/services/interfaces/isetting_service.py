from abc import ABC, abstractmethod


class ISettingService(ABC):

    @abstractmethod
    async def create_htb_netem_qdiscs(payload):
        pass

    @abstractmethod
    async def update_htb(payload):
        pass

    @abstractmethod
    async def update_netem(payload):
        pass

    @abstractmethod
    async def delete_htb_netem_qdiscs():
        pass
