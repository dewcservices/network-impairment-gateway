from abc import ABC, abstractmethod


class ISettingService(ABC):

    @abstractmethod
    async def create_htb_netem_qdiscs(self, payload):
        pass

    @abstractmethod
    async def update_htb(self, payload):
        pass

    @abstractmethod
    async def update_netem(self, payload):
        pass

    @abstractmethod
    async def delete_htb_netem_qdiscs(self):
        pass
