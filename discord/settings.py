# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2021-present Dolfies

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

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from .enums import FriendFlags, StickerAnimationOptions, Theme, UserContentFilter, try_enum
from .guild_folder import GuildFolder

if TYPE_CHECKING:
    from .guild import Guild
    from .state import ConnectionState


class Settings:
    """Represents the Discord client settings.

    Attributes
    ----------
    afk_timeout: :class:`int`
        How long (in seconds) the user needs to be AFK until Discord
        sends push notifications to your mobile device.
    allow_accessibility_detection: :class:`bool`
        Whether or not to allow Discord to track screen reader usage.
    animate_emojis: :class:`bool`
        Whether or not to animate emojis in the chat.
    contact_sync_enabled: :class:`bool`
        Whether or not to enable the contact sync on Discord mobile.
    convert_emoticons: :class:`bool`
        Whether or not to automatically convert emoticons into emojis.
        e.g. :-) -> 😃
    default_guilds_restricted: :class:`bool`
        Whether or not to automatically disable DMs between you and
        members of new guilds you join.
    detect_platform_accounts: :class:`bool`
        Whether or not to automatically detect accounts from services
        like Steam and Blizzard when you open the Discord client.
    developer_mode: :class:`bool`
        Whether or not to enable developer mode.
    disable_games_tab: :class:`bool`
        Whether or not to disable the showing of the Games tab.
    enable_tts_command: :class:`bool`
        Whether or not to allow tts messages to be played/sent.
    gif_auto_play: :class:`bool`
        Whether or not to automatically play gifs that are in the chat.
    inline_attachment_media: :class:`bool`
        Whether or not to display attachments when they are uploaded in chat.
    inline_embed_media: :class:`bool`
        Whether or not to display videos and images from links posted in chat.
    locale: :class:`str`
        The :rfc:`3066` language identifier of the locale to use for the language
        of the Discord client.
    message_display_compact: :class:`bool`
        Whether or not to use the compact Discord display mode.
        native_phone_integration_enabled: :class:`bool`
        Whether or not to enable the new Discord mobile phone number friend
        requesting features.
    render_embeds: :class:`bool`
        Whether or not to render embeds that are sent in the chat.
    render_reactions: :class:`bool`
        Whether or not to render reactions that are added to messages.
    show_current_game: :class:`bool`
        Whether or not to display the game that you are currently playing.
    stream_notifications_enabled: :class:`bool`
        Unknown.
    timezone_offset: :class:`int`
        The timezone offset to use.
    view_nsfw_guilds: :class:`bool`
        Whether or not to show NSFW guilds on iOS.
    """

    if TYPE_CHECKING:  # Fuck me
        afk_timeout: int
        allow_accessibility_detection: bool
        animate_emojis: bool
        animate_stickers: StickerAnimationOptions
        contact_sync_enabled: bool
        convert_emoticons: bool
        default_guilds_restricted: bool
        detect_platform_accounts: bool
        developer_mode: bool
        disable_games_tab: bool
        enable_tts_command: bool
        explicit_content_filter: UserContentFilter
        friend_source_flags: FriendFlags
        gif_auto_play: bool
        guild_positions: List[Guild]
        inline_attachment_media: bool
        inline_embed_media: bool
        locale: str
        message_display_compact: bool
        native_phone_integration_enabled: bool
        render_embeds: bool
        render_reactions: bool
        restricted_guilds: List[Guild]
        show_current_game: bool
        stream_notifications_enabled: bool
        theme: Theme
        timezone_offset: int
        view_nsfw_guilds: bool

    def __init__(self, *, data, state: ConnectionState) -> None:
        self._state = state
        self._update(data)

    def __repr__(self) -> str:
        return '<Settings>'

    def _update(self, data: Dict[str, Any]) -> None:
        RAW_VALUES = {
            'afk_timeout',
            'allow_accessibility_detection',
            'animate_emojis',
            'contact_sync_enabled',
            'convert_emoticons',
            'default_guilds_restricted',
            'detect_platform_accounts',
            'developer_mode',
            'disable_games_tab',
            'enable_tts_command',
            'inline_attachment_media',
            'inline_embed_media',
            'locale',
            'message_display_compact',
            'native_phone_integration_enabled',
            'render_embeds',
            'render_reactions',
            'show_current_game',
            'stream_notifications_enabled',
            'timezone_offset',
            'view_nsfw_guilds',
        }

        for key, value in data.items():
            if key in RAW_VALUES:
                setattr(self, key, value)
            else:
                setattr(self, '_' + key, value)

    @property
    def animate_stickers(self) -> StickerAnimationOptions:
        """Whether or not to animate stickers in the chat."""
        return try_enum(StickerAnimationOptions, self._animate_stickers)

    @property
    def explicit_content_filter(self) -> UserContentFilter:
        """The filter for explicit content in all messages."""
        return try_enum(UserContentFilter, self._explicit_content_filter)

    @property
    def friend_source_flags(self) -> FriendFlags:
        """Who can add you as a friend."""
        return FriendFlags._from_dict(self._friend_source_flags)

    @property
    def guild_folders(self) -> List[GuildFolder]:
        """A list of guild folders."""
        state = self._state
        return [GuildFolder(data=folder, state=state) for folder in self._guild_folders]

    @property
    def guild_positions(self) -> List[Guild]:
        """A list of guilds in order of the guild/guild icons that are on
        the left hand side of the UI.
        """
        return list(filter(None, map(self._get_guild, self._guild_positions)))

    @property
    def restricted_guilds(self) -> List[Guild]:
        """A list of guilds that you will not receive DMs from."""
        return list(filter(None, map(self._get_guild, self._restricted_guilds)))

    @property
    def theme(self) -> Theme:
        """The theme of the Discord UI."""
        return try_enum(Theme, self._theme)

    def _get_guild(self, id: int) -> Optional[Guild]:
        return self._state._get_guild(int(id))
