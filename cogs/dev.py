import logging
import traceback
import contextlib
import io
import textwrap

import internals
from internals.cog_jumpstart import *


class Dev(Cog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.evars = {}

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx):
        """syncs slash commands"""
        synced = await self.bot.tree.sync()
        await ctx.reply(f"Synced {len(synced)} commands.")

    @commands.command(name="eval")
    @commands.is_owner()
    async def _eval(self, ctx, *, code: str):
        """Stripped down version of the eval command in Cap+"""
        if code.startswith("`"):
            code = code.lstrip("```py\n").rstrip("```")
        stdout = io.StringIO()
        code = "async def evaluated():\n" + textwrap.indent(code, "    ")
        if ctx.message.reference:
            r = ctx.message.reference.resolved
        else:
            r = None
        self.evars = {
            **self.evars,
            "ctx": ctx,
            "bot": self.bot,
            "user": ctx.author,
            "guild": ctx.guild,
            "channel": ctx.channel,
            "author": ctx.author,
            "reply": r,
            "logger": self.logger.getChild("eval")
        }
        with contextlib.redirect_stdout(stdout):
            try:
                exec(code, self.evars)
                returned = str(await self.evars["evaluated"]())
            except Exception as e:
                stdout = io.StringIO("".join(traceback.format_exception(type(e), e, e.__traceback__)))
                returned = "Error!"
        stdout = stdout.getvalue()
        pages = [stdout[i:i + 1891] for i in range(0, len(stdout), 1891)]
        self.evars['_'] = returned
        if len(pages) == 0:
            pages = ["No output."]
        if returned[:75] == returned:
            ret = returned
        else:
            ret = returned[:75] + "..."
        pages = [f"{e}```\n\n```py\n{ret}" for e in pages]
        pag = internals.ButtonPaginator(pages=pages,
                                        force_embed=True,
                                        color=discord.Colour.yellow(),
                                        title="Eval",
                                        prefix="```py\n",
                                        suffix="```")
        await pag.start(ctx)


    @commands.command(name="raise")
    @commands.is_owner()
    async def _raise(self, ctx):
        raise Exception("Test")


setup = ms(Dev)