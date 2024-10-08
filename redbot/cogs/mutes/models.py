from dataclasses import dataclass
from typing import Dict, Optional

import discord


@dataclass
class MuteResponse:
    success: bool
    reason: Optional[str]
    user: discord.Member


@dataclass
class ChannelMuteResponse(MuteResponse):
    channel: discord.abc.GuildChannel
    old_overs: Optional[Dict[str, bool]]
    voice_mute: bool
