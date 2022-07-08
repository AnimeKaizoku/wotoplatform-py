import pytest
from wotoplatform import WotoClient
from wotoplatform.types.errors import (
    NotModified
)
from wotoplatform.types import RawResponse
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
    
    try:
        await client.start()
    except Exception:
        await client.stop()
        raise
    me = await client.get_me()
    print(me)

    try:
        assert await client.change_user_bio(__TEST_BIO_VALUE01__)
    except NotModified: pass
    except Exception:
        await client.stop()
        raise
    
    me = await client.get_me()
    assert me.bio == __TEST_BIO_VALUE01__

    try:
        assert await client.change_names(
            first_name=__TEST_FIRST_NAME_VALUE01__, 
            last_name=__TEST_LAST_NAME_VALUE01__,
        )
    except NotModified: pass
    except Exception:
        await client.stop()
        raise

    me = await client.get_me()
    assert me.first_name == __TEST_FIRST_NAME_VALUE01__
    assert me.last_name == __TEST_LAST_NAME_VALUE01__

    user_info = await client.get_user_info(the_config.username)
    assert user_info.username == the_config.username
    assert user_info.first_name == __TEST_FIRST_NAME_VALUE01__
    assert user_info.last_name == __TEST_LAST_NAME_VALUE01__
    assert user_info.bio == __TEST_BIO_VALUE01__

    try:
        await client.set_user_favorite('anime', 'One Piece')
    except NotModified: pass

    fav01 = await client.get_user_favorite('anime')

    assert fav01.favorite_value == 'One Piece'
    
    from wotoplatform.types.usersData import (__ACTION_USER__, __BATCH_GET_USER_FAVORITE__)
    fav01_raw_data = {
        'user_id' : 0,
        'favorite_key': 'anime'
    }
    fav01_raw_resp = await client.send_raw_batch(__ACTION_USER__, __BATCH_GET_USER_FAVORITE__, fav01_raw_data)
    
    assert isinstance(fav01_raw_resp, RawResponse)

    try:
        await client.set_user_favorite('light-novel', 'Mushoku Tensei')
    except NotModified: pass

    fav02 = await client.get_user_favorite('light novel')

    assert fav02.favorite_value == 'Mushoku Tensei'
    
    await client.stop()


@pytest.mark.asyncio
async def test_raw_batch_execution():
    client = WotoClient(
        the_config.username, 
        the_config.password, 
        the_config.host,
        the_config.port,
    )
    
    try:
        await client.start()
    except Exception:
        await client.stop()
        raise
    
    from wotoplatform.types.usersData import (__ACTION_USER__, __BATCH_GET_USER_FAVORITE__)
    fav01_raw_data = {
        'user_id' : 0,
        'favorite_key': 'anime'
    }
    fav01_raw_resp = await client.send_raw_batch(__ACTION_USER__, __BATCH_GET_USER_FAVORITE__, fav01_raw_data)
    
    assert isinstance(fav01_raw_resp, RawResponse)
    
    try:
        from wotoplatform.types.groupsData import (__ACTION_GROUPS__, __BATCH_GET_GROUP_INFO_BY_ID__)
        group_id_data = {
            'group_id': 'GR-125412'
        }
        group_info_raw_resp = await client.send_raw_batch(__ACTION_GROUPS__, __BATCH_GET_GROUP_INFO_BY_ID__, group_id_data)
        assert isinstance(group_info_raw_resp, RawResponse)
    except Exception as e:
        print(e) 
    
    
    await client.stop()
