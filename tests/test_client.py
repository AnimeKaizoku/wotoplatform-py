import pytest
from wotoplatform import WotoClient
from .myconfig import the_config

@pytest.mark.asyncio
async def test_woto_client():
    client = WotoClient(
        the_config.username, 
        the_config.password, 
        the_config.host,
        the_config.port,
    )
    await client.start()
    print(await client.get_me())

