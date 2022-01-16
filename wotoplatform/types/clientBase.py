
from . import Scaffold

class ClientBase:
    async def send(self, _: Scaffold) -> bytes:
        pass
