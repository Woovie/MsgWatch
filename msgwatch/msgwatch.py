import discord
from datetime import datetime
from redbot.core import commands, Config, checks

class MsgWatch(commands.Cog):
    """Various tools to look for malicious activity in Discord messages."""
    def __init__(self):
        self.config = Config.get_conf(self, 5555, force_registration=True)
        default_guild = {
            "log_channel": None,
            "command_channel": None,
            "roles": [],
            "monitored_users": []
        }
        self.config.register_guild(**default_guild)
    
    @commands.group()
    @checks.admin()
    async def msg_watch(self, ctx):
        """All message watching functions."""
        pass

    @msg_watch.command()
    async def log_channel(self, ctx, channel: discord.TextChannel):
        """Set the message logging output channel."""
        await self.config.guild(ctx.guild).log_channel.set(channel.id)
        await ctx.send(f"Channel for logging has been set to {channel.mention}.")
    
    @msg_watch.command()
    async def command_channel(self, ctx, channel: discord.TextChannel):
        """Set the message logging command input channel."""
        await self.config.guild(ctx.guild).command_channel.set(channel.id)
        await ctx.send(f"Channel for commands has been set to {channel.mention}.")

    @msg_watch.command()
    async def add_role(self, ctx, role: discord.Role):
        """Set a role to be monitored for mentions."""
        await self.config.guild(ctx.guild).roles.append(role.id)
        await ctx.send(f"Added role '{role.name}' to monitored roles.")

    @msg_watch.command()
    async def rem_role(self, ctx, role: discord.Role):
        """Remove a role from being monitored for mentions."""
        await self.config.guild(ctx.guild).roles.remove(role.id)
        await ctx.send(f"Removed role '{role.name}' from monitored roles.")
    
    @msg_watch.command()
    @checks.mod()
    async def add_user(self, ctx, user: discord.User):
        """Add a user to per-message monitoring."""
        await self.config.guild(ctx.guild).monitored_users.append(user.id)
        await ctx.send(f"Added user {user.mention} to monitored users.")
    
    @msg_watch.command()
    @checks.mod()
    async def rem_user(self, ctx, user: discord.User):
        """Remove a user from per-message monitoring."""
        await self.config.guild(ctx.guild).monitored_users.remove(user.id)
        await ctx.send(f"Removed user {user.mention} from monitored users.")

    @commands.Cog.listener()
    async def on_message(self, ctx):
        settings = await self.config.guild(ctx.guild).all()
        if ctx.author.bot:
            return
        if ctx.guild is None:
            return
        if ctx.author.id in settings["monitored_users"]:
            embed = discord.Embed(
                title = f"[MONITORED USER] {ctx.author.mention} ({ctx.author.id})",
                description = ctx.content,
                timestamp = datetime.utcnow()
            )
            await ctx.guild.get_channel(settings["log_channel"]).send(embed=embed)

        user_mentions = ctx.mentions
        if len(user_mentions) > 0:
            mentioned = False
            for user in user_mentions:
                roles = user.roles
                for role in roles:
                    if role.id in settings["roles"]:
                        embed = discord.Embed(
                            title = f"[MEMBER MENTION] {ctx.author.mention} ({ctx.author.id})",
                            description = ctx.content,
                            timestamp = datetime.utcnow()
                        )
                        await ctx.guild.get_channel(settings["log_channel"]).send(embed=embed)
                        mentioned = True
                        break
                if mentioned:
                    break