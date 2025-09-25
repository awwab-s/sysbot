import discord
from discord.ext import commands
import time

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="hello", description="Greet the bot")
    async def hello(self, ctx):
        await ctx.send(f"Hello {ctx.author.name}! 👋")
    
    @commands.hybrid_command(name="ping", description="Check the bot's latency")
    async def ping(self, ctx):
        await ctx.send(f"Pong! 🏓 Latency: {round(self.bot.latency * 1000)}ms")
        
    @commands.command()
    async def test(self, ctx):
        await ctx.send(f"Tf are you testing {ctx.author.name}? 😂")
    
    @commands.command()
    async def spam(self, ctx):
        await ctx.send("<:arab_flushed:1335270974089724016>" * 7)
    
    @commands.hybrid_command(name="uptime", description="Check bot uptime")
    async def uptime(self, ctx):
        uptime = time.time() - self.bot.start_time
        uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime))
        await ctx.send(f"⏱️ Uptime: `{uptime_str}`")

    @commands.hybrid_command(name="help", description="Show help message")
    async def help(self, ctx):
        help_text = """
        **Available Commands:**
        `!hello` - Greet the bot
        `!help` - Show this help message
        `!ping` - Check the bot's latency
        `!userinfo [@user]` - Get info about a user
        `!serverinfo` - Get info about the server
        `!ask <question>` - Ask a question
        `!study <minutes>` - Start a study session  
        `!status` - Check remaining time in your study session  
        `!cancelstudy` - Cancel your active study session
        """
        await ctx.send(help_text)
    
    @commands.hybrid_command(name="userinfo", description="Get info about a user")
    async def userinfo(self, ctx, member: commands.MemberConverter = None):
        member = member or ctx.author
        embed = discord.Embed(
            title=f"User Info - {member}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Name", value=member.name, inline=True)
        embed.add_field(name="Joined", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Created", value=member.created_at.strftime("%Y-%m-%d"), inline=True)

        await ctx.send(embed=embed)


    @commands.hybrid_command(name="serverinfo", description="Get info about the server")
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(
          title=f"Server Info - {guild.name}",
          color=discord.Color.green()
        )
        embed.add_field(name="Server ID", value=guild.id, inline=True)
        embed.add_field(name="Owner", value=guild.owner, inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Created On", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))
