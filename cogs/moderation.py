import traceback
from internals.classes import GuildConfig
from internals.cog_jumpstart import *
from internals import ignore_exc

class cog(Cog):
    no_reason_msg = "No reason provided."
    action_to_title = {
        "ban": "User banned.",
        "mute": "User muted.",
        "kick": "User kicked",
        "unmute": "User unmuted."
    }
    def cog_check(self, ctx) -> bool:
        return ctx.author.guild_permissions.kick_members  
        # usually, mods have kick_members at the very least, but not always ban.

    async def log_action(self, action: str, author: discord.Member, user: discord.User, reason: str = None):
        reason = reason or self.no_reason_msg
        if reason == self.no_reason_msg:
            reason += " | Moderators: ~~please add a reason using the `/reason` command~~ TODO"  # TODO
        config = await GuildConfig.from_guild(author.guild.id)
        guild = author.guild
        channel = guild.get_channel(config.mchannel)
        if not channel:
            return
        
        embed = discord.Embed(
            title=self.action_to_title.get(action, "Unknown action."),
            description=f"Reason: {reason}",
            color=discord.Color.red()
        )
        embed.add_field(name="Moderator", value=f"{author} ({author.mention} | {author.id})", inline=False)
        embed.add_field(name="User", value=f"{user} ({user.mention} | {user.id})", inline=False)
        await channel.send(embed=embed)

        

    @commands.hybrid_group(name="mod")
    async def mod(self, ctx):
        pass

    @mod.command(name="ban")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def mod_ban(self, ctx: commands.Context, member: discord.Member, reason: str=None):
        reason = reason or self.no_reason_msg
        # check role hierarchy
        if not ctx.author.top_role.position > member.top_role.position:
            return await ctx.reply(f"You can't ban members that are above or equal to you in the role hierarchy.", ephemeral=True)
        embed = discord.Embed(
            title=f"You've been banned from {ctx.guild.name}!",
            description=f"Reason:```\n{reason}```",
            color=discord.Color.red()
            )
        if not ctx.guild.me.top_role.position > member.top_role.position:
            return await ctx.reply("I am not high enough in the role hierarchy to perform that action.", ephemeral=True)
        await ignore_exc(member.send(embed=embed))
        await ctx.guild.ban(member, reason=reason + f" | {ctx.author.id}")
        await ctx.reply(f"Successfully banned {member}!")

    @commands.Cog.listener("on_member_ban")
    async def on_member_ban(self, guild: discord.Guild, user: discord.User):
        try:
            config = await GuildConfig.from_guild(guild.id)
            if config.mchannel == 0:
                return
            
            try:
                entry = [entry async for entry in guild.audit_logs(limit=1, user=guild.me, action=discord.AuditLogAction.ban)][0]
            except:
                return  # not dealing with this crap
            reason = entry.reason.split(" | ")
            reason = reason[0:-1]
            reason = " | ".join(reason)
            await self.log_action(action="ban", author=guild.get_member(int(entry.reason.split(" | ")[-1])), user=user, reason=reason)
        except Exception as e:
            self.logger.error("".join(traceback.format_exception(type(e), e, e.__traceback__)))


setup = ms(cog)