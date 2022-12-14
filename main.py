import discord
import asyncio

from discord import app_commands
from discord.ext import commands
from internals import Bot, PaginatedEmbedHelpCommand

import logging
import sys
import config

# set up logging.
logger = logging.getLogger("Bot")
formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] : %(message)s", datefmt="%H:%M:%S")
handlers = [
    logging.StreamHandler(),
    logging.FileHandler(filename="latest.log", mode="w")
]
logger.setLevel(config.loglevel)
for h in handlers:
    h.setFormatter(formatter)
    logger.addHandler(h)
logger.info("Initializing...")

intents = discord.Intents.default()
intents.message_content = True
bot = Bot(
    command_prefix=config.prefix,
    intents=intents,
    status=discord.Status.dnd,
    activity=discord.Game("You got games on your phone?"),
    help_command=PaginatedEmbedHelpCommand(),
    description="An indev moderation bot",
    allowed_mentions=discord.AllowedMentions.none(),
    owner_pass=config.owner_pass
)


# Extension 'cogs.contextmenu' raised an error: TypeError: context menus cannot be defined inside a class
@app_commands.context_menu(name="report")
@app_commands.guilds(discord.Object(id=1030371410637488159))
async def reportmenu(interaction: discord.Interaction, message: discord.Message):
    channel: discord.TextChannel = bot.get_channel(1050882293146865705)
    embed = discord.Embed(
        title=f"Report on {message.author!r} by {interaction.user!r}",
        description=f"Content:```\n{discord.utils.escape_markdown(message.content)}```"
    )
    embed.add_field(name="Message link", value=message.jump_url, inline=False)
    embed.add_field(name="User info", value=f"```\nID = {message.author.id}\nJoined: {message.author.joined_at}\nCreated: {message.author.created_at}```", inline=True)
    embed.add_field(name="Reporter info", value=f"```\nID = {interaction.user.id}\nJoined: {interaction.user.joined_at}\nCreated: {interaction.user.created_at}```", inline=True)
    t = await channel.create_thread(name=str(interaction.user.id),
                                    type=discord.ChannelType.private_thread)
    await t.send(interaction.user.mention, embed=embed)


async def main():
    if config.loglevel == logging.DEBUG - 1:
        discord.utils.setup_logging(
            handler=discord.utils.MISSING,
            formatter=formatter,
            level=logging.DEBUG,
            root=False,
        )
    async with bot:
        logger.info("Starting...")
        await bot.start(config.token)



if __name__ == "__main__":
    asyncio.run(main())
