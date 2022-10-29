#  WotoPlatform-Py - A Python library for interacting with WotoPlatform API.
#  Copyright (C) 2021-2022  ALiwoto - <woto@kaizoku.cyou> <https://github.com/ALiwoto>
#
#  This file is part of WotoPlatform-Py.
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import typing
from ..base_types.scaffold import (
    DScaffold,
    RScaffold,
    ResultScaffold,
)

__BATCH_CHECK_VERSION__ = 'check_version'
__ACTION_VERSION__ = 1

class VersionData(DScaffold):
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

