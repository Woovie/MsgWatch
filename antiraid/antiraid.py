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

    # @antiraid.command()
    # @checks.mod()
    # async def enable_channel(self, ctx, channel_id):
    #     channel = ctx.guild.get_channel(int(channel_id))
    #     if type(channel) == discord.TextChannel:
    #         await channel.edit(slowmode_delay=300)
    #         self.channels.append(channel_id)
    #         await ctx.channel.send(f"Altered {channel_id}.\nresponse: {response}")
    #     else:
    #         await ctx.channel.send(f"Invalid channel ID provided or other failure:\ntype(ctx.guild.get_channel(channel_id)): {type(channel)}")

    @antiraid.command()
    @checks.mod()
    async def enable(self, ctx):
        if not self.enabled:
            channels = ctx.guild.channels
            for channel in channels:
                if type(channel) == discord.TextChannel:
                    if channel.slowmode_delay == 0:
                        self.channels.append(channel.id)
                        await channel.edit(slowmode_delay=300)
            self.enabled = True
            await ctx.channel.send("AntiRaid enabled.")
        else:
            await ctx.channel.send("AntiRaid already enabled.")

    @antiraid.command()
    @checks.mod()
    async def disable(self, ctx):
        if self.enabled:
            for channel_id in self.channels:
                channel = ctx.guild.get_channel(int(channel_id))
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
        for slowmode, count in enumerate(antiraid_hash):
            embed_antiraid.add_field(name=f"{slowmode} seconds", value=f"{count} channels")
        await ctx.channel.send('', embed=embed_antiraid)
        #Discord data
        server_hash = {}
        embed_discord = discord.Embed(title='Server Information', type='rich', color=discord.Color(0xF5C800))
        embed_discord.set_footer(text='Data from within guild')
        channels = ctx.guild.channels
        for channel in channels:
            if type(channel) == discord.TextChannel:
                slowmode = str(channel.slowmode_delay)
                if not slowmode in server_hash:
                    server_hash[slowmode] = 1
                else:
                    server_hash[slowmode] += 1
        for slowmode, count in enumerate(server_hash):
            embed_discord.add_field(name=f"{slowmode} seconds", value=f"{count} channels")
        await ctx.channel.send('', embed=embed_discord)