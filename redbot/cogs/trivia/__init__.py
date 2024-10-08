"""Package for Trivia cog."""

from redbot.cogs.trivia.log import LOG
from redbot.cogs.trivia.session import TriviaSession
from redbot.cogs.trivia.trivia import UNIQUE_ID, InvalidListError, Trivia, get_core_lists, get_list
from redbot.core.bot import Red


async def setup(bot: Red) -> None:
    """Load Trivia."""
    await bot.add_cog(Trivia(bot))


__all__ = [
    "LOG",
    "TriviaSession",
    "Trivia",
    "UNIQUE_ID",
    "InvalidListError",
    "get_core_lists",
    "get_list",
    "setup",
]
