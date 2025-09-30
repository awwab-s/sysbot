import aiohttp
import discord
from discord.ext import commands
import config
import asyncio
import time


def to_arabic_numerals(num: int) -> str:
        english = "0123456789"
        arabic = "٠١٢٣٤٥٦٧٨٩"
        return "".join(arabic[english.index(d)] for d in str(num))
    
    

class Quran(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.token = None
        self.token_expiry = 0
        self.chapters = {}
  
    async def get_token(self):
        """Fetch OAuth2 token from Quran API"""
        now = time.time()
        if self.token and now < self.token_expiry:
            return self.token  # still valid
        
        async with self.session.post(
            f"{config.QURAN_TOKEN_URL}/oauth2/token",
            auth=aiohttp.BasicAuth(config.QURAN_CLIENT_ID, config.QURAN_CLIENT_SECRET),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data="grant_type=client_credentials&scope=content",
        ) as resp:
            if resp.status != 200:
                print(f"❌ Failed to get token: {resp.status}")
                return None
            token_data = await resp.json()
            self.token = token_data.get("access_token")
            self.token_expiry = now + token_data.get("expires_in", 3600) - 60  # buffer 60s
            return self.token
    
    # async def api_request(self, endpoint, params=None):
    #     """Make authenticated request to Quran API"""
    #     token = await self.get_token()
    #     headers = {
    #         "x-auth-token": token,
    #         "x-client-id": config.QURAN_CLIENT_ID,
    #     }
    #     url = f"{config.QURAN_BASE_URL}{endpoint}"
    #     async with self.session.get(url, headers=headers, params=params) as resp:
    #         if resp.status == 401:
    #             # Token expired, refresh
    #             self.token = None
    #             return await self.api_request(endpoint, params)
    #         return await resp.json()
    
    async def api_request(self, endpoint, params=None):
        """Make request to Quran API without OAuth"""
        url = f"{config.QURAN_BASE_URL}{endpoint}"
        async with self.session.get(url, params=params) as resp:
            if resp.status != 200:
                print(f"❌ API call failed: {resp.status}")
                return None
            return await resp.json()
    
    @commands.command(name="pingq")
    async def pingq(self, ctx):
        await ctx.send("Quran cog is alive ✅")
        
    async def get_chapters(self):
        """Fetch and cache surah names once"""
        if self.chapters:
            return self.chapters

        data = await self.api_request("/chapters")
        if not data or "chapters" not in data:
            print("❌ Could not fetch chapters list.")
            return {}

        for ch in data["chapters"]:
            self.chapters[ch["id"]] = ch
        return self.chapters

    @commands.command(name="quran", help="Fetch specific ayah from Qur'an")
    async def quran(self, ctx, reference: str):
        """Fetch specific ayah from Qur'an"""
        try:
            surah, ayah = map(int, reference.split(":"))
            print(surah, ayah)
        except ValueError:
            await ctx.send("⚠️ Use the format <surah_no>:<ayah_no>")
            return
        
        # Get surah
        chapters = await self.get_chapters()
        surah_info = chapters.get(surah, {})
        surah_name_en = surah_info.get("name_simple", f"{surah}")
        surah_name_ar = surah_info.get("name_arabic", "")
        surah_revelation = surah_info.get("revelation_place", "")
        
        # Get verse
        data = await self.api_request(f"/verses/by_chapter/{surah}", params={"fields": "text_uthmani"})
        if not data or "verses" not in data:
            await ctx.send("❌ Could not fetch surah.")
            return
        
        verses = data["verses"]
        verse = next((v for v in verses if v["verse_number"] == ayah), None)
        if not verse:
            await ctx.send("❌ Could not fetch ayah.")
            return
        
        text = verse.get("text_uthmani", "No text available.")
        ayah_marker = f" ﴿{to_arabic_numerals(ayah)}﴾"
        embed = discord.Embed(
            title=f"Surah: {surah_name_en} ({surah_name_ar})",
            description=f"**{text}{ayah_marker}**",
            color=discord.Color.gold()
        )
        embed.set_footer(
            text=f"Revealed in {surah_revelation.capitalize()}"
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Quran(bot))