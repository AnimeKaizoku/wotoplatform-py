import pytest
from wotoplatform import WotoClient
from wotoplatform.types.errors.serverErrors import NotModified
from .myconfig import the_config

__TEST_BIO_VALUE01__ = 'This is my test bio'
__TEST_FIRST_NAME_VALUE01__ = 'ALiwoto'
__TEST_LAST_NAME_VALUE01__ = 'lastname~'

@pytest.mark.asyncio
async def test_woto_client01():
    client = WotoClient(
        the_config.username, 
        the_config.password, 
        the_config.host,
        the_config.port,
    )
    await client.start()
    print(await client.get_me())

    try:
        assert await client.change_user_bio(__TEST_BIO_VALUE01__)
    except NotModified: pass
    
    me = await client.get_me()
    assert me.bio == __TEST_BIO_VALUE01__

    try:
        assert await client.change_names(
            first_name=__TEST_FIRST_NAME_VALUE01__, 
            last_name=__TEST_LAST_NAME_VALUE01__,
        )
    except NotModified: pass

    me = await client.get_me()
    assert me.first_name == __TEST_FIRST_NAME_VALUE01__
    assert me.last_name == __TEST_LAST_NAME_VALUE01__

    user_info = await client.get_user_info(the_config.username)
    assert user_info.username == the_config.username
    assert user_info.first_name == __TEST_FIRST_NAME_VALUE01__
    assert user_info.last_name == __TEST_LAST_NAME_VALUE01__
    assert user_info.bio == __TEST_BIO_VALUE01__

