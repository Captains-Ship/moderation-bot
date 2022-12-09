import discord
from discord import app_commands

from internals.cog_jumpstart import *
from internals import GuildConfig

class Conf(Cog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.guild_configs_cache = {}

    def ensure_cached(self, gid: int) -> GuildConfig:
        if self.guild_configs_cache.get(str(gid)):
            return self.guild_configs_cache.get(str(gid))
        else:
            self.guild_configs_cache[str(gid)] = GuildConfig()
            return self.guild_configs_cache.get(str(gid))

    @commands.hybrid_group(name="config", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def _config(self, ctx):
        await ctx.reply("See the help page for `config`")

    @_config.group("set")
    @commands.has_permissions(administrator=True)
    async def c_set(self, ctx):
        pass

    @c_set.command(name="add_dynamic_slowmode")
    @commands.has_permissions(administrator=True)
    async def c_set_adddslow(self, ctx, channel: discord.TextChannel):
        conf = self.ensure_cached(ctx.guild.id)
        conf.dynamic_slowmode_channels.add(channel.id)
        await ctx.reply(f"Added <#{channel.id}> to the dynamic slowmode list", ephemeral=True)


    @c_set.command(name="del_dynamic_slowmode")
    @commands.has_permissions(administrator=True)
    async def c_set_deldslow(self, ctx, channel: discord.TextChannel):
        conf = self.ensure_cached(ctx.guild.id)
        conf.dynamic_slowmode_channels.remove(channel.id)
        await ctx.reply(f"removed <#{channel.id}> from the dynamic slowmode list", ephemeral=True)


    @_config.command("get")
    @commands.has_permissions(administrator=True)
    @app_commands.choices(key=GuildConfig.possible)
    async def c_get(self, ctx, key: str):
        conf = self.ensure_cached(ctx.guild.id)
        value = getattr(conf, key)
        if isinstance(value, set):
            value = ", ".join([f"<#{id}>" for id in value])
        await ctx.reply(value or "None", ephemeral=True)


setup = ms(Conf)