
import typing
from .scaffold import (
    DScaffold,
    RScaffold,
    ResultScaffold,
)

__BATCH_CHECK_VERSION__ = 'check_version'
__ACTION_VERSION__ = 1

class VersionData(DScaffold):
    data_unique_id: str = ''
    user_agent: str = 'wp-client'
    version_key: str = '2.1.1.5014'
    version_hash: str = 'f302bd7ffacbd295194f86620002b8250e8e9be0233a8055bcebc82c8612843ff9e0f09e42015d5e75581cc93d4c29a91388ed411641b543c8fb7b5a26a2a8b8'
    client_id: str = 'cli-12345678910'

    def get_action(self) -> int:
        return __ACTION_VERSION__
    
    def get_single_batch(self) -> str:
        return __BATCH_CHECK_VERSION__
    
    def get_response_type(self) -> type:
        return VersionResponse


class VersionResult(ResultScaffold):
    is_acceptable: bool = False
    server_time: str = ''
    
class VersionResponse(RScaffold):
    result: typing.Optional[VersionResult]

