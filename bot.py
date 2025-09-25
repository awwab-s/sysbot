import discord
from discord.ext import commands
import config
import asyncio
import time

intents = discord.Intents.default()
intents.message_content = True  # Required for reading messages

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents, help_command=None)

extensions = [
    "cogs.general",
    "cogs.ai",
    "cogs.study",
]

# Track bot start time
bot.start_time = None  

@bot.event
async def on_ready():
    await bot.tree.sync()
    bot.start_time = time.time()
    print(f"Logged in as {bot.user}")
    bot.loop.create_task(console_input())

@bot.event
async def on_command(ctx):
    print(f"[DEBUG] Command '{ctx.command}' triggered by {ctx.author} in {ctx.channel}")
    print("> ", end="", flush=True)
        
async def console_input():
    await bot.wait_until_ready()
    channel = bot.get_channel(config.CHANNEL_ID)
    while True:
        msg = await asyncio.get_event_loop().run_in_executor(None, input, "> ")
        if msg.strip():
            await channel.send(msg)

async def main():
    async with bot:
        for ext in extensions:
            await bot.load_extension(ext)
        await bot.start(config.TOKEN)

if __name__ == "__main__":
    from server import keep_alive
    keep_alive()
    asyncio.run(main())
