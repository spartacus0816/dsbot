discord.py
==========

.. image:: https://img.shields.io/pypi/v/discord.py-self.svg
   :target: https://pypi.python.org/pypi/discord.py-self
   :alt: PyPI version info
.. image:: https://img.shields.io/pypi/pyversions/discord.py-self.svg
   :target: https://pypi.python.org/pypi/discord.py-self
   :alt: PyPI supported Python versions

A modern, easy to use, feature-rich, and async ready API wrapper for Discord written in Python.

Fork Changes
------------

- Fixed self-bot issues with ``message.content`` and ``message.embed``.
- Obfuscated user-agent
- I haven't tried this with a regular bot. You're welcome to try, but I do not recommend it.

**Credits:**

- `u/pogofetch <https://www.reddit.com/user/pogofetch/>`_ for most of the changes.
- `karibiusk <https://stackoverflow.com/users/15139805/karibiusk/>`_ for some food for thought.
- `Maxx0911 <https://www.reddit.com/user/Maxx0911/>`_ for more food for thought.

Key Features
-------------

- Modern Pythonic API using ``async`` and ``await``.
- Proper rate limit handling.
- 100% coverage of the supported Discord API.
- Optimised in both speed and memory.

Installing
----------

**Python 3.5.3 or higher is required**

To install the library without full voice support, you can just run the following command:

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U discord.py-self

    # Windows
    py -3 -m pip install -U discord.py-self

Otherwise to get voice support you should run the following command:

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U "discord.py-self[voice]"

    # Windows
    py -3 -m pip install -U discord.py-self[voice]


To install the development version, do the following:

.. code:: sh

    $ git clone https://github.com/dolfies/discord.py-self
    $ cd discord.py
    $ python3 -m pip install -U .[voice]


Optional Packages
~~~~~~~~~~~~~~~~~~

* PyNaCl (for voice support)

Please note that on Linux installing voice you must install the following packages via your favourite package manager (e.g. ``apt``, ``dnf``, etc) before running the above commands:

* libffi-dev (or ``libffi-devel`` on some systems)
* python-dev (e.g. ``python3.6-dev`` for Python 3.6)

Quick Example
--------------

.. code:: py

    import discord

    class MyClient(discord.Client):
        async def on_ready(self):
            print('Logged on as', self.user)

        async def on_message(self, message):
            # don't respond to ourselves
            if message.author == self.user:
                return

            if message.content == 'ping':
                await message.channel.send('pong')

    client = MyClient()
    client.run('token', bot=False)

Bot Example
~~~~~~~~~~~~~

.. code:: py

    import discord
    from discord.ext import commands

    bot = commands.Bot(command_prefix='>')

    @bot.command()
    async def ping(ctx):
        await ctx.send('pong')

    bot.run('token', bot=False)

You can find more examples in the examples directory.

Links
------

- `Documentation <https://discordpy.readthedocs.io/en/latest/index.html>`_
- `Discord API <https://discord.gg/discord-api>`_
