import discord, json, time
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
    async def enable(self, ctx, test = None):
        if not self.enabled:
            channels = ctx.guild.channels
            text_channels = []
            for channel in channels:
                if type(channel) == discord.TextChannel and channel.slowmode_delay == 0:
                    text_channels.append(channel)
            count = 0
            message = await ctx.channel.send(f"Starting AntiRaid process, this will take a few seconds...\n{count}/{len(text_channels)} channels processed.")
            for channel in text_channels:
                self.channels.append(channel.id)
                if not test:
                    await channel.edit(slowmode_delay=300)
                else:
                    time.sleep(1)
                count += 1
                if count % 20 == 0 or count == len(text_channels):
                    await message.edit(content=f"Starting AntiRaid process, this will take a few seconds...\n{count}/{len(text_channels)} channels processed.")
            if not test:
                self.enabled = True
            await ctx.channel.send("AntiRaid enabled.")
        else:
            await ctx.channel.send("AntiRaid already enabled.")

    @antiraid.command()
    @checks.mod()
    async def disable(self, ctx, test = None):
        if self.enabled:
            for channel_id in self.channels:
                channel = ctx.guild.get_channel(int(channel_id))
                if not test:
                    await channel.edit(slowmode_delay=0)
            self.enabled = False
            self.channels.clear()
            await ctx.channel.send("AntiRaid disabled.")
        else:
            await ctx.channel.send("AntiRaid already disabled.")

    @antiraid.command()
    @checks.mod()
    async def status(self, ctx):
        #AntiRaid data
        antiraid_hash = {}
        embed_antiraid = discord.Embed(title='AntiRaid Information', type='rich', color=discord.Color(0xF5C800))
        embed_antiraid.set_footer(text='Data from within AntiRaid class')
        embed_antiraid.add_field(name='self.enabled', value=self.enabled)
        for channel_id in self.channels:
            channel = ctx.guild.get_channel(int(channel_id))
            slowmode = str(channel.slowmode_delay)
            if not slowmode in antiraid_hash:
                antiraid_hash[slowmode] = 1
            else:
                antiraid_hash[slowmode] += 1
        for slowmode in antiraid_hash:
            embed_antiraid.add_field(name=f"{slowmode} seconds", value=f"{str(antiraid_hash[slowmode])} channels")
        await ctx.channel.send('', embed=embed_antiraid)
        #Discord data
        server_hash = {}
        embed_discord = discord.Embed(title='Server Information', type='rich', color=discord.Color(0xF5C800))
        embed_discord.set_footer(text='Slowmode data from within guild')
        channels = ctx.guild.channels
        for channel in channels:
            if type(channel) == discord.TextChannel:
                slowmode = str(channel.slowmode_delay)
                if not slowmode in server_hash:
                    server_hash[slowmode] = 1
                else:
                    server_hash[slowmode] += 1
        for slowmode in server_hash:
            embed_discord.add_field(name=f"{slowmode} seconds", value=f"{str(server_hash[slowmode])} channels")
        await ctx.channel.send('', embed=embed_discord)