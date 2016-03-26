# -*- coding: utf-8 -*-
"""
The MIT License (MIT)

Copyright (c) 2015-2016 Rapptz

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

from copy import deepcopy
from . import utils
from .permissions import Permissions
from .enums import ChannelType
from collections import namedtuple
from .mixins import Hashable

Overwrites = namedtuple('Overwrites', 'id allow deny type')

class Channel(Hashable):
    """Represents a Discord server channel.

    Supported Operations:

    +-----------+---------------------------------------+
    | Operation |              Description              |
    +===========+=======================================+
    | x == y    | Checks if two channels are equal.     |
    +-----------+---------------------------------------+
    | x != y    | Checks if two channels are not equal. |
    +-----------+---------------------------------------+
    | hash(x)   | Returns the channel's hash.           |
    +-----------+---------------------------------------+
    | str(x)    | Returns the channel's name.           |
    +-----------+---------------------------------------+

    Attributes
    -----------
    name : str
        The channel name.
    server : :class:`Server`
        The server the channel belongs to.
    id : str
        The channel ID.
    topic : Optional[str]
        The channel's topic. None if it doesn't exist.
    is_private : bool
        ``True`` if the channel is a private channel (i.e. PM). ``False`` in this case.
    position : int
        The position in the channel list. This is a number that starts at 0. e.g. the
        top channel is position 0. The position varies depending on being a voice channel
        or a text channel, so a 0 position voice channel is on top of the voice channel
        list.
    type : :class:`ChannelType`
        The channel type. There is a chance that the type will be ``str`` if
        the channel type is not within the ones recognised by the enumerator.
    bitrate : int
        The channel's preferred audio bitrate in bits per second.
    changed_roles
        A list of :class:`Roles` that have been overridden from their default
        values in the :attr:`Server.roles` attribute.
    voice_members
        A list of :class:`Members` that are currently inside this voice channel.
        If :attr:`type` is not :attr:`ChannelType.voice` then this is always an empty array.
    """

    def __init__(self, **kwargs):
        self._update(**kwargs)
        self.voice_members = []

    def __str__(self):
        return self.name

    def _update(self, **kwargs):
        self.name = kwargs.get('name')
        self.server = kwargs.get('server')
        self.id = kwargs.get('id')
        self.topic = kwargs.get('topic')
        self.is_private = False
        self.position = kwargs.get('position')
        self.bitrate = kwargs.get('bitrate')
        self.type = kwargs.get('type')
        try:
            self.type = ChannelType(self.type)
        except:
            pass

        self.changed_roles = []
        self._permission_overwrites = []
        everyone_index = 0
        everyone_id = self.server.default_role.id

        for index, overridden in enumerate(kwargs.get('permission_overwrites', [])):
            overridden_id = overridden['id']
            self._permission_overwrites.append(Overwrites(**overridden))

            if overridden.get('type') == 'member':
                continue

            if overridden_id == everyone_id:
                # the @everyone role is not guaranteed to be the first one
                # in the list of permission overwrites, however the permission
                # resolution code kind of requires that it is the first one in
                # the list since it is special. So we need the index so we can
                # swap it to be the first one.
                everyone_index = index

            # this is pretty inefficient due to the deep nested loops unfortunately
            role = utils.find(lambda r: r.id == overridden_id, self.server.roles)
            if role is None:
                continue

            denied = overridden.get('deny', 0)
            allowed = overridden.get('allow', 0)
            override = deepcopy(role)
            override.permissions.handle_overwrite(allowed, denied)
            self.changed_roles.append(override)

        # do the swap
        tmp = self._permission_overwrites
        if tmp:
            tmp[everyone_index], tmp[0] = tmp[0], tmp[everyone_index]

    @property
    def is_default(self):
        """bool : Indicates if this is the default channel for the :class:`Server` it belongs to."""
        return self.server.id == self.id

    @property
    def mention(self):
        """str : The string that allows you to mention the channel."""
        return '<#{0.id}>'.format(self)

    @property
    def created_at(self):
        """Returns the channel's creation time in UTC."""
        return utils.snowflake_time(self.id)

    def permissions_for(self, member):
        """Handles permission resolution for the current :class:`Member`.

        This function takes into consideration the following cases:

        - Server owner
        - Server roles
        - Channel overrides
        - Member overrides
        - Whether the channel is the default channel.

        Parameters
        ----------
        member : :class:`Member`
            The member to resolve permissions for.

        Returns
        -------
        :class:`Permissions`
            The resolved permissions for the member.
        """

        # The current cases can be explained as:
        # Server owner get all permissions -- no questions asked. Otherwise...
        # The @everyone role gets the first application.
        # After that, the applied roles that the user has in the channel
        # (or otherwise) are then OR'd together.
        # After the role permissions are resolved, the member permissions
        # have to take into effect.
        # After all that is done.. you have to do the following:

        # If manage permissions is True, then all permissions are set to
        # True. If the channel is the default channel then everyone gets
        # read permissions regardless.

        # The operation first takes into consideration the denied
        # and then the allowed.

        if member.id == self.server.owner.id:
            return Permissions.all()

        default = self.server.default_role
        base = deepcopy(default.permissions)

        # Apply server roles that the member has.
        for role in member.roles:
            base.value |= role.permissions.value

        # Server-wide Manage Roles -> True for everything
        if base.manage_roles:
            base = Permissions.all()

        member_role_ids = set(map(lambda r: r.id, member.roles))

        # Apply channel specific role permission overwrites
        for overwrite in self._permission_overwrites:
            if overwrite.type == 'role':
                if overwrite.id in member_role_ids:
                    base.handle_overwrite(allow=overwrite.allow, deny=overwrite.deny)

        # Apply member specific permission overwrites
        for overwrite in self._permission_overwrites:
            if overwrite.type == 'member' and overwrite.id == member.id:
                base.handle_overwrite(allow=overwrite.allow, deny=overwrite.deny)

        if base.manage_roles:
            # This point is essentially Channel-specific Manage Roles.
            tmp = Permissions.all_channel()
            base.value |= tmp.value

        if self.is_default:
            base.read_messages = True

        return base

class PrivateChannel(Hashable):
    """Represents a Discord private channel.

    Supported Operations:

    +-----------+-------------------------------------------------+
    | Operation |                   Description                   |
    +===========+=================================================+
    | x == y    | Checks if two channels are equal.               |
    +-----------+-------------------------------------------------+
    | x != y    | Checks if two channels are not equal.           |
    +-----------+-------------------------------------------------+
    | hash(x)   | Returns the channel's hash.                     |
    +-----------+-------------------------------------------------+
    | str(x)    | Returns the string "Direct Message with <User>" |
    +-----------+-------------------------------------------------+

    Attributes
    ----------
    user : :class:`User`
        The user you are participating with in the private channel.
    id : str
        The private channel ID.
    is_private : bool
        ``True`` if the channel is a private channel (i.e. PM). ``True`` in this case.
    """

    __slots__ = ['user', 'id', 'is_private']

    def __init__(self, user, id, **kwargs):
        self.user = user
        self.id = id
        self.is_private = True

    def __str__(self):
        return 'Direct Message with {0.name}'.format(self.user)

    @property
    def created_at(self):
        """Returns the private channel's creation time in UTC."""
        return utils.snowflake_time(self.id)

    def permissions_for(self, user):
        """Handles permission resolution for a :class:`User`.

        This function is there for compatibility with :class:`Channel`.

        Actual private messages do not really have the concept of permissions.

        This returns all the Text related permissions set to true except:

        - send_tts_messages: You cannot send TTS messages in a PM.
        - manage_messages: You cannot delete others messages in a PM.
        - mention_everyone: There is no one to mention in a PM.

        Parameters
        -----------
        user : :class:`User`
            The user to check permissions for.

        Returns
        --------
        :class:`Permissions`
            The resolved permissions for the user.
        """

        base = Permissions.text()
        base.send_tts_messages = False
        base.manage_messages = False
        base.mention_everyone = False
        return base


