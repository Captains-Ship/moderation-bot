import asyncio
import internals.classes

async def main():
    gc = await internals.classes.GuildConfig.from_guild(1)
    print(gc.mchannel == 0)


if __name__ == "__main__":
    asyncio.run(main())