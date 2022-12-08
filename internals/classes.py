from discord.ext import commands
import discord


__all__ = (
    "Bot",
    "PaginatedEmbedHelpCommand"
)

import internals


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class PaginatedEmbedHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self) -> None:
        paginator = internals.ButtonPaginator(
            pages=self.paginator.pages,
            color=0x600e35,  # type: ignore
            force_embed=True,
            title="Help",
            )
        await paginator.start(self.context)