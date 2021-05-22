.. currentmodule:: discord

.. |commands| replace:: [:ref:`ext.commands <discord_ext_commands>`]
.. |tasks| replace:: [:ref:`ext.tasks <discord_ext_tasks>`]

.. _whats_new:

Changelog
============

This page keeps a detailed human friendly rendering of what's new and changed
in specific versions.

v1.8.0
-------
- Fixes ``guild.me``.
- Partially fixes ``guild.members`` (only if you have manage_guild perm).
- Fixes large guild events.

v1.7.8
-------
- Removes all bot-only methods + functions.
- Un-deprecates user-only functions.
- Removes bot and deprecation notices from docstrings.

v1.7.7
-------
- Add lazy loading patch to group dms (fixes #11).

v1.7.6
-------
- Code cleanup.
- Bug fixes.
- Deprecate regular bot accounts.
- Deprecate ``bot=False``.

v1.7.5
-------

- Fix all self-bot issues.
- Add user lazy-loading.
