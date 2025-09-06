import discord
from discord.ext import commands
import aiohttp
import asyncio
import config
import time

class AskAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()  # reuse session for all requests
        self.daily_limit = 50
        self.requests_today = 0
        self.reset_time = time.time() + 24*60*60  # reset every 24h
        self.max_response_length = 1000  # truncate overly long replies

    async def query_api(self, prompt: str):
        """Send prompt to Mistral 7B Instruct via OpenRouter"""
        url="https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {config.CHAT_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": config.CHAT_MODEL,
            "messages": [
              {
                "role": "user",
                "content": prompt
                }
              ],
            "max_tokens": 500,  # keep responses short
        }

        # Retry logic for rate limits
        for attempt in range(3):
            async with self.session.post(url, headers=headers, json=payload) as resp:
                if resp.status == 429:
                    await asyncio.sleep(2 ** attempt)  # 2s, 4s, 8s
                    continue
                elif resp.status != 200:
                    return f"❌ API Error {resp.status}"
                data = await resp.json()
                # Prefer content; fallback to reasoning if content is empty
                choice = data["choices"][0]["message"]
                reply = choice.get("content", "").strip()
                if not reply:
                    reply = choice.get("reasoning", "").strip()
                return reply or "⚠️ No response from AI"
        return "⚠️ Too many requests, try again later."

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)  # 1 request / 15s per user
    async def ask(self, ctx, *, question: str):
        """Ask the AI a question"""
        if ctx.channel.id != config.CHANNEL_ID:
            await ctx.send("⚠️ This command does not work in the channel.")
            return
        
        now = time.time()
        if now > self.reset_time:
            self.requests_today = 0
            self.reset_time = now + 24*60*60

        if self.requests_today >= self.daily_limit:
            await ctx.send("⚠️ Daily request limit reached. Try again tomorrow.")
            return

        await ctx.send("🤖 Thinking...")

        response = await self.query_api(question)
        self.requests_today += 1

        # Trim overly long responses
        # if len(response) > self.max_response_length:
        #     response = response[:self.max_response_length] + "\n[...] (response truncated)"

        await ctx.send(response)
    
    async def cog_unload(self):
        """Close the session when the cog is unloaded"""
        await self.session.close()

async def setup(bot):
    await bot.add_cog(AskAI(bot))
