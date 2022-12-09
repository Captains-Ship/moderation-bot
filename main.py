import discord
import asyncio
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
