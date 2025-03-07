from discord.ext.commands import Bot

COGS = ["ready", "topic_channel"]


class NelChan(Bot):
    def __init__(self, commands_prefix: str = "nel,"):
        super().__init__(command_prefix=commands_prefix)

        for cog in COGS:
            self.load_extension("nelchan.bot.cogs." + cog)
