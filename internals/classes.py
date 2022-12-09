import traceback

from discord.app_commands import Choice
from discord.ext import commands
import discord
import os
import logging



import config

logger = logging.getLogger("Bot")

__all__ = (
    "Bot",
    "PaginatedEmbedHelpCommand",
    "GuildConfig"
)

import internals


class PassModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)




class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.owner_pass = kwargs.pop("owner_pass")
        super().__init__(*args, **kwargs)
        if self.owner_pass.endswith("???PRINTPASS"):
            self.owner_pass = self.owner_pass.replace("???PRINTPASS", "")
            logger.info(f"Random password: {self.owner_pass}")

    async def setup_hook(self) -> None:
        for cog in os.listdir("./cogs"):
            if not cog.endswith(".py"):
                continue
            try:
                await self.load_extension(f"cogs.{cog[:-3]}")
                logger.info(f"Loaded cog cogs/{cog}")
            except Exception as e:
                logger.error(f"Failed to load cogs/{cog}:\n{e}")

    async def on_command_error(self, context, exception) -> None:
        if isinstance(exception, discord.ext.commands.NotOwner):
            ...  # TODO: self.bot.owner_pass

        else:
            logger.error("".join(traceback.format_exception(type(exception), exception, exception.__traceback__)))
            embed = discord.Embed(
                title="Uh oh...",
                description=f"We got an error!\n\"{exception}\"\nReport this at [the support server](https://discord.gg/gDcBMNeXc4)",
                color=discord.Colour.red()
            )
            embed.set_thumbnail(url=context.bot.user.display_avatar.url)
            await context.reply(embed=embed, ephemeral=True)

class PaginatedEmbedHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self) -> None:
        paginator = internals.ButtonPaginator(
            pages=self.paginator.pages,
            color=0x600e35,  # type: ignore
            force_embed=True,
            title="Help",
        )
        await paginator.start(self.context)


class GuildConfig:
    possible = [Choice(name="Dynamic Slowmode Channels", value="dynamic_slowmode_channels"), Choice(name="Automod level", value="automod_level"), Choice(name="Prefix", value="prefix")]
    def __init__(self, **kwargs):
        self.values = {
            "dynamic_slowmode_channels": set(),
            "automod_level": 0,
            "prefix": config.prefix,
            **kwargs
        }
    def __getattr__(self, item):
        if self.values.get(item) is not None:
            return self.values.get(item)
        logger.getChild("GuildConfig").warning(f"Unknown setting {item!r} requested.")
        return f"{item!r} is not a config value."