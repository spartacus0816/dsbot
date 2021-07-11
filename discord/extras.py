# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2015-present Dolfies

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from base64 import b64encode
import json
import logging
import re

log = logging.getLogger(__name__)

async def get_build_number(session): # Thank you Discord-S.C.U.M
    """Fetches client build number"""
    try:
        login_page_request = await session.request('get', 'https://discord.com/login', headers={'Accept-Encoding': 'gzip, deflate'}, timeout=10)
        login_page = await login_page_request.text()
        build_url = 'https://discord.com/assets/' + re.compile(r'assets/+([a-z0-9]+)\.js').findall(login_page)[-2] + '.js'
        build_request = await session.request('get', build_url, headers={'Accept-Encoding': 'gzip, deflate'}, timeout=10)
        build_file = await build_request.text()
        build_index = build_file.find('buildNumber') + 14
        return int(build_file[build_index:build_index + 5])
    except:
        log.warning('Could not fetch client build number.')
        return 88863

async def get_user_agent(session):
    """Fetches the latest Windows 10/Chrome user-agent."""
    try:
        request = await session.request('get', 'https://jnrbsn.github.io/user-agents/user-agents.json', timeout=10)
        response = json.loads(await request.text())
        return response[0]
    except:
        log.warning('Could not fetch user-agent.')
        return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'

async def get_browser_version(session):
    """Fetches the latest Windows 10/Chrome version."""
    try:
        request = await session.request('get', 'https://omahaproxy.appspot.com/all.json', timeout=10)
        response = json.loads(await request.text())
        if response[0]['versions'][4]['channel'] == 'stable':
            return response[0]['versions'][4]['version']
    except:
        log.warning('Could not fetch browser version.')
        return '91.0.4472.77'

class ContextProperties: # Thank you Discord-S.C.U.M
    """Represents the Discord X-Context-Properties header.

        .. container:: operations

        .. describe:: str(x)

            Returns the location name.

        .. describe:: bool(x)

            Checks if the properties have a location.

        .. describe:: x == y

            Checks if the properties are equal to other properties.

        .. describe:: x != y

            Checks if the properties are not equal to other properties.

        .. describe:: hash(x)

            Returns the hash of the properties.
    """

    __slots__ = ('_data', '_value')

    def __init__(self, data):
        self._data = data
        self._value = self._encode_data(data)

    def _encode_data(self, data):
        library = {
            'Friends': 'eyJsb2NhdGlvbiI6IkZyaWVuZHMifQ==',
            'ContextMenu': 'eyJsb2NhdGlvbiI6IkNvbnRleHRNZW51In0=',
            'User Profile': 'eyJsb2NhdGlvbiI6IlVzZXIgUHJvZmlsZSJ9',
            'Add Friend': 'eyJsb2NhdGlvbiI6IkFkZCBGcmllbmQifQ==',
            'Guild Header': 'eyJsb2NhdGlvbiI6Ikd1aWxkIEhlYWRlciJ9',
            'Group DM': 'eyJsb2NhdGlvbiI6Ikdyb3VwIERNIn0=',
            'DM Channel': 'eyJsb2NhdGlvbiI6IkRNIENoYW5uZWwifQ==',
            '/app': 'eyJsb2NhdGlvbiI6ICIvYXBwIn0='
        }

        try:
            return library[data['location']]
        except KeyError:
            return b64encode(json.dumps(data).encode()).decode('utf-8')

    @classmethod
    def _from_empty(cls):
        data = {}
        return cls(data)

    @classmethod
    def _from_friends_page(cls):
        data = {
            'location': 'Friends'
        }
        return cls(data)

    @classmethod
    def _from_context_menu(cls):
        data = {
            'location': 'ContextMenu'
        }
        return cls(data)

    @classmethod
    def _from_user_profile(cls):
        data = {
            'location': 'User Profile'
        }
        return cls(data)

    @classmethod
    def _from_add_friend_page(cls):
        data = {
            'location': 'Add Friend'
        }
        return cls(data)

    @classmethod
    def _from_guild_header_menu(cls):
        data = {
            'location': 'Guild Header'
        }
        return cls(data)

    @classmethod
    def _from_group_dm(cls):
        data = {
            'location': 'Group DM'
        }
        return cls(data)

    @classmethod
    def _from_dm_channel(cls):
        data = {
            'location': 'DM Channel'
        }
        return cls(data)

    @classmethod
    def _from_app(cls):
        data = {
            'location': '/app'
        }
        return cls(data)

    @classmethod
    def _from_accept_invite_page(cls, *, guild_id, channel_id, channel_type):
        data = {
            'location': 'Accept Invite Page',
            'location_guild_id': guild_id,
            'location_channel_id': channel_id,
            'location_channel_type': channel_type
        }
        return cls(data)

    @classmethod
    def _from_join_guild_popup(cls, *, guild_id, channel_id, channel_type):
        data = {
            'location': 'Join Guild',
            'location_guild_id': guild_id,
            'location_channel_id': channel_id,
            'location_channel_type': channel_type
        }
        return cls(data)

    @classmethod
    def _from_invite_embed(cls, *, guild_id, channel_id, channel_type, message_id):
        data = {
            'location': 'Invite Button Embed',
            'location_guild_id': guild_id,
            'location_channel_id': channel_id,
            'location_channel_type': channel_type,
            'location_message_id': message_id
        }
        return cls(data)

    @property
    def value(self):
        return self._value

    @property
    def location(self):
        return self._data.get('location', None)

    @property
    def guild_id(self):
        return self._data.get('location_guild_id', None)

    @property
    def channel_id(self):
        return self._data.get('location_channel_id', None)

    @property
    def channel_type(self):
        return self._data.get('location_channel_type', None)

    @property
    def message_id(self):
        return self._data.get('location_message_id', None)

    def __bool__(self):
        return self.value is not None

    def __str__(self):
        return self._data.get('location', 'None')

    def __repr__(self):
        return '<ContextProperties location={0.location}>'.format(self)

    def __eq__(self, other):
        return isinstance(other, ContextProperties) and self._data == other._data

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self._data)
