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
]

# Track bot start time
bot.start_time = None  

@bot.event
async def on_ready():
    bot.start_time = time.time()
    print(f"Logged in as {bot.user}")
    bot.loop.create_task(console_input())

@bot.event
async def on_command(ctx):
    print(f"[DEBUG] Command '{ctx.command}' triggered by {ctx.author} in {ctx.channel}")
    print("> ", end="", flush=True)

@bot.event
async def on_disconnect():
    channel = bot.get_channel(config.CHANNEL_ID)
    if channel:
        uptime = time.time() - bot.start_time if bot.start_time else 0
        uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime))
        await channel.send(f"🛑 Bot offline. Uptime: `{uptime_str}`")
        print(f"🛑 Bot offline. Uptime: `{uptime_str}`")
        
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
        try:
            await bot.start(config.TOKEN)
        except KeyboardInterrupt:
            print(f"Keyboard Interrupt. Bot offline.")
            await bot.close()

if __name__ == "__main__":
    from server import keep_alive
    keep_alive()
    asyncio.run(main())
