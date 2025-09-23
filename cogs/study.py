import discord
from discord.ext import commands
import asyncio
import time

class Study(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # active_sessions will store timers per user
        # format: {user_id: {"end_time": <timestamp>, "task": <asyncio.Task>}}
        self.active_sessions = {}

    @commands.command()
    async def study(self, ctx, minutes: int):
        """Start a study session for <minutes> minutes."""
        user_id = ctx.author.id

        if user_id in self.active_sessions:
            await ctx.send(f"⚠️ {ctx.author.mention} You already have an active session! Use `!cancelstudy` first.")
            return

        end_time = time.time() + minutes * 60
        task = asyncio.create_task(self._timer(ctx, minutes))

        self.active_sessions[user_id] = {"end_time": end_time, "task": task}
        await ctx.send(f"⏰ {ctx.author.mention} Your {minutes}-minute study session has started! Stay focused 💪")

    async def _timer(self, ctx, minutes: int):
        """Internal task to wait and then remind the user."""
        await asyncio.sleep(minutes * 60)
        user_id = ctx.author.id
        # Check if still active (not cancelled)
        if user_id in self.active_sessions:
            await ctx.send(f"🔔 {ctx.author.mention} Time’s up! You studied for {minutes} minutes. Take a break ☕")
            self.active_sessions.pop(user_id, None)

    @commands.command()
    async def cancelstudy(self, ctx):
        """Cancel your current study session."""
        user_id = ctx.author.id

        if user_id not in self.active_sessions:
            await ctx.send(f"⚠️ {ctx.author.mention} You don’t have any active study sessions.")
            return

        task = self.active_sessions[user_id]["task"]
        task.cancel()
        self.active_sessions.pop(user_id, None)
        await ctx.send(f"🛑 {ctx.author.mention} Your study session has been cancelled.")

    @commands.command()
    async def status(self, ctx):
        """Check how much time is left in your session."""
        user_id = ctx.author.id

        if user_id not in self.active_sessions:
            await ctx.send(f"⚠️ {ctx.author.mention} You don’t have any active sessions.")
            return

        end_time = self.active_sessions[user_id]["end_time"]
        remaining = int(end_time - time.time())

        minutes, seconds = divmod(remaining, 60)
        await ctx.send(f"⏳ {ctx.author.mention} You have {minutes}m {seconds}s left.")

async def setup(bot):
    await bot.add_cog(Study(bot))
