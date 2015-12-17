.. currentmodule:: discord

.. _migrating-to-async:

Migrating to v0.10.0
======================

v0.10.0 is one of the biggest breaking changes in the library due to massive
fundamental changes in how the library operates.

The biggest major change is that the library has dropped support to all versions prior to
Python 3.4.2. This was made to support ``asyncio``, in which more detail can be seen
:issue:`in the corresponding issue <50>`. To reiterate this, the implication is that
**python version 2.7 and 3.3 are no longer supported**.

Below are all the other major changes from v0.9.0 to v0.10.0.

.. _migrating-event-registration:

Event Registration
--------------------

All events before were registered using :meth:`Client.event`. While this is still
possible, the events must be decorated with ``@asyncio.coroutine``.

Before:

.. code-block:: python

    @client.event
    def on_message(message):
        pass

After:

.. code-block:: python

    @client.event
    @asyncio.coroutine
    def on_message(message):
        pass

Or in Python 3.5+:

.. code-block:: python

    @client.event
    async def on_message(message):
        pass

Because there is a lot of typing, a utility decorator (:meth:`Client.async_event`) is provided
for easier registration. For example:

.. code-block:: python

    @client.async_event
    def on_message(message):
        pass


Be aware however, that this is still a coroutine and your other functions that are coroutines must
be decorated with `` @asyncio.coroutine`` or be ``async def``.

.. _migrating_event_changes:

Event Changes
--------------

Some events in v0.9.0 were considered pretty useless due to having no separate states. The main
events that were changed were the ``_update`` events since previously they had no context on what
was changed.

Before:

.. code-block:: python

    def on_channel_update(channel): pass
    def on_member_update(member): pass
    def on_status(member): pass
    def on_server_role_update(role): pass
    def on_voice_state_update(member): pass


After:

.. code-block:: python

    def on_channel_update(before, after): pass
    def on_member_update(before, after): pass
    def on_server_role_update(before, after): pass
    def on_voice_state_update(before, after): pass

Note that ``on_status`` was removed. If you want its functionality, use :func:`on_member_update`.
See :ref:`discord-api-events` for more information.


.. _migrating-coroutines:

Coroutines
-----------

The biggest change that the library went through is that almost every function in :class:`Client`
was changed to be a `coroutine <https://docs.python.org/3/library/asyncio-task.html>`_. Functions
that are marked as a coroutine in the documentation must be awaited from or yielded from in order
for the computation to be done. For example...

Before:

.. code-block:: python

    client.send_message(message.channel, 'Hello')

After:

.. code-block:: python

    yield from client.send_message(message.channel, 'Hello')

    # or in python 3.5+
    await client.send_message(message.channel, 'Hello')

In order for you to ``yield from`` or ``await`` a coroutine then your function must be decorated
with ``@asyncio.coroutine`` or ``async def``.

.. _migrating-enums:

Enumerators
------------

Due to dropping support for versions lower than Python 3.4.2, the library can now use
`enumerators <https://docs.python.org/3/library/enum.html>`_ in places where it makes sense.

The common places where this was changed was in the server region, member status, and channel type.

Before:

.. code-block:: python

    server.region == 'us-west'
    member.status == 'online'
    channel.type == 'text'

After:

.. code-block:: python

    server.region == discord.ServerRegion.us_west
    member.status = discord.Status.online
    channel.type == discord.ChannelType.text

The main reason for this change was to reduce the use of finnicky strings in the API as this
could give users a false sense of power. More information can be found in the :ref:`discord-api-enums` page.

.. _migrating-properties:

Properties
-----------

A lot of function calls that returned constant values were changed into Python properties for ease of use
in format strings.

The following functions were changed into properties:

+----------------------------------------+--------------------------------------+
|                 Before                 |                After                 |
+----------------------------------------+--------------------------------------+
| ``user.avatar_url()``                  | :attr:`User.avatar_url`              |
+----------------------------------------+--------------------------------------+
| ``user.mention()``                     | :attr:`User.mention`                 |
+----------------------------------------+--------------------------------------+
| ``channel.mention()``                  | :attr:`Channel.mention`              |
+----------------------------------------+--------------------------------------+
| ``channel.is_default_channel()``       | :attr:`Channel.is_default`           |
+----------------------------------------+--------------------------------------+
| ``role.is_everyone()``                 | :attr:`Role.is_everyone`             |
+----------------------------------------+--------------------------------------+
| ``server.get_default_role()``          | :attr:`Server.default_role`          |
+----------------------------------------+--------------------------------------+
| ``server.icon_url()``                  | :attr:`Server.icon_url`              |
+----------------------------------------+--------------------------------------+
| ``server.get_default_channel()``       | :attr:`Server.default_channel`       |
+----------------------------------------+--------------------------------------+
| ``message.get_raw_mentions()``         | :attr:`Message.raw_mentions`         |
+----------------------------------------+--------------------------------------+
| ``message.get_raw_channel_mentions()`` | :attr:`Message.raw_channel_mentions` |
+----------------------------------------+--------------------------------------+

.. _migrating-running:

Running the Client
--------------------

In earlier versions of discord.py, ``client.run()`` was a blocking call to the main thread
that called it. In v0.10.0 it is still a blocking call but it handles the event loop for you.
However, in order to do that you must pass in your credentials to :meth:`Client.run`.

Basically, before:

.. code-block:: python

    client.login('email', 'password')
    client.run()

After:

.. code-block:: python

    client.run('email', 'password')

This is a utility function that abstracts the event loop for you. There's no need for
the run call to be blocking and out of your control. Indeed, if you want control of the
event loop then doing so is quite straightforward:

.. code-block:: python

    import discord
    import asyncio

    client = discord.Client()

    @asyncio.coroutine
    def main_task():
        yield from client.login('email', 'password')
        yield from client.connect()

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main_task())
    except:
        loop.run_until_complete(client.logout())
    finally:
        loop.close()



