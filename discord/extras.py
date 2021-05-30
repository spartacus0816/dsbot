# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2015-present Rapptz

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

import logging
import re
import requests
from time import sleep

from .ua_parser import user_agent_parser

log = logging.getLogger(__name__)

async def get_build_number(session):
    """Fetches client build number"""
    try:
        login_page_request = await session.request('get', 'https://discord.com/login', headers = {'Accept-Encoding': 'gzip, deflate'})
        login_page = await login_page_request.text()
        build_url = 'https://discord.com/assets/' + re.compile(r'assets/+([a-z0-9]+)\.js').findall(login_page)[-2] + '.js'
        build_request = await session.request('get', build_url, headers = {'Accept-Encoding': 'gzip, deflate'})
        build_file = await build_request.text()
        build_index = build_file.find('buildNumber') + 14
        return int(build_file[build_index:build_index + 5])
    except:
        log.warning('Could not fetch client build number.')
        return 86447

def get_user_agent():
    """Fetches the latest Chrome for Windows 10 user-agent."""
    try:
        url = 'https://jnrbsn.github.io/user-agents/user-agents.json'
        response = requests.get(url, timeout = 5)
        user_agents = response.json()
        return user_agents[0]
    except:
        log.warning('Could not fetch user-agent.')
        return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'

def parse_user_agent(user_agent):
    parsed = user_agent_parser.Parse(user_agent)
    browser = [parsed['user_agent']['major'], parsed['user_agent']['minor'], parsed['user_agent']['patch']]
    return browser
