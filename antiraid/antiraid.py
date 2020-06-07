import discord, json
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

    @commands.group()
    @checks.admin()
    async def antiraid(self, ctx):
        """All antiraid functions."""
        pass

    @antiraid.command()
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

    @antiraid.command()
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
            await ctx.channel.send("AntiRaid alreadydisabled.")

    @antiraid.command()
    @checks.mod()
    async def status(self, ctx):
        channels = ctx.guild.channels
        embed_antiraid = discord.Embed(title='AntiRaid Information', type='rich', color=discord.Color(0xF5C800))
        embed_antiraid.add_field(name='self.enabled', value=self.enabled)
        embed_antiraid.add_field(name='self.channels', value=json.dumps(self.channels))
        embed_discord = discord.Embed(title='Server Information', description='Channels with a delay', type='rich', color=discord.Color(0xF5C800))
        for channel in channels:
            if type(channel) == discord.TextChannel:
                if channel.slowmode_delay > 0:
                    embed_discord.add_field(name=channel.name, value=channel.slowmode_delay)
        await ctx.channel.send('', embed=embed_antiraid)
        await ctx.channel.send('', embed=embed_discord)