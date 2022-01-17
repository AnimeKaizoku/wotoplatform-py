import pytest
from wotoplatform import WotoClient
from wotoplatform.types.errors.serverErrors import NotModified
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
    try:
        print(await client.change_user_bio('hello, this a test'))
    except NotModified:
        print('bio is already that value')

