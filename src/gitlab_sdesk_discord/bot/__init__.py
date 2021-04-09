from __future__ import annotations

import os
import sys

from discord.ext import commands

from .loop_helpers import asyncio_run
from .sdesk import SDesk


async def run_bot(bot: commands.Bot) -> None:
    try:
        await bot.start(os.environ["GITLAB_SDESK_DISCORD_TOKEN"])
    finally:
        if not bot.is_closed():
            await bot.close()


def main() -> int:
    bot = commands.Bot()
    bot.add_cog(SDesk(bot))
    asyncio_run(run_bot(bot))
    return 0


if __name__ == "__main__":
    sys.exit(main())
