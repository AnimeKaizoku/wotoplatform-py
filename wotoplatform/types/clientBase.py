
from . import Scaffold

class ClientBase:
    async def send(self, _: Scaffold) -> bytes:
        pass

    async def send_raw_batch(self, batch_name: str, data):
        pass
