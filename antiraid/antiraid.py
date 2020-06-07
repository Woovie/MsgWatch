import discord
from datetime import datetime
from redbot.core import commands, Config, checks

class AntiRaid(commands.Cog):
    """Various tools to look for malicious activity in Discord messages."""
    def __init__(self):
        self.config = Config.get_conf(self, 5555, force_registration=True)
        default_guild = {}
        self.channels = []
        self.enabled = False
        self.config.register_guild(**default_guild)

    @checks.mod()
    async def enable(self, ctx):
        if not self.enabled:
            channels = ctx.guild.channels
            for channel in channels:
                if type(channel) == discord.TextChannel:
                    if channel.slowmode_delay == 0:
                        self.channels.append(channel.id)
                        channel.slowmode_delay = 300
            self.enabled = True
            await ctx.channel.send("AntiRaid enabled.")
        else:
            await ctx.channel.send("AntiRaid already enabled.")

    @checks.mod()
    async def disable(self, ctx):
        if self.enabled:
            for channel_id in self.channels:
                channel = ctx.guild.get_channel(channel_id)
                channel.slowmode_delay = 0
            self.enabled = False
            self.channels.clear()
            await ctx.channel.send("AntiRaid disabled.")
        else:
            await ctx.channel.send("AntiRaid already disabled.")
