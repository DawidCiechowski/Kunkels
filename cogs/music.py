import re
from typing import Optional
import asyncio
import urllib
import json
import os
from collections import deque

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import youtube_dl
from youtubesearchpython import VideosSearch


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""
        
    @staticmethod
    def _is_youtube_url(text: str) -> list:
        regex = "^http*[s]://.+\.youtube\.com/*watch?"
        return re.findall(regex, text)
    
    @staticmethod
    def _get_url(text: str) -> str:
        search = VideosSearch(text, limit=1)
        return search.result()['result'][0]["link"]
    
    @staticmethod
    def _get_name(text: str) -> str:
        if YTDLSource._is_youtube_url(text):
            params = {"format": "json", "url": text}
            query = urllib.parse.urlencode(params)
            url = "https://www.youtube.com/oembed?" + query
            
            with urllib.request.urlopen(url) as response:
                response_text = response.read()
                data = json.loads(response_text.decode())
                return data["title"]
        else:
            search = VideosSearch(text, limit=1)
            return search.result()['result'][0]["title"]
    @classmethod
    async def from_url(cls, argument: str, *, loop=None, stream=False):
        url = None
        # ytdl_format_options = {
        #     'format': 'bestaudio/best',
        #     'restrictfilenames': True,
        #     'noplaylist': True,
        #     'nocheckcertificate': True,
        #     'ignoreerrors': False,
        #     'logtostderr': False,
        #     'quiet': True,
        #     'extract_audio':True,
        #     'no_warnings': True,
        #     'default_search': 'auto',
        #     'postprocessors': [{
        #         'key': "FFmpegExtractAudio",
        #         'preferredcodec': 'mp3',
        #         'preferredquality': '192',
        #     }],
        #     'prefer_ffmpeg': True,
        # }
        # ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

        if YTDLSource._is_youtube_url(argument):
            url = argument
        else:
            url = YTDLSource._get_url(argument)
        
        # loop = loop or asyncio.get_event_loop()
        # data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        # if 'entries' in data:
        #     # take first item from a playlist
        #     data = data['entries'][0]
        # filename = data['title'] if stream else ytdl.prepare_filename(data)
        if os.path.exists("./song.mp3"):
            os.remove("./song.mp3")
        os.system(f'youtube-dl -x -f bestaudio/best --audio-format mp3 -o "song.%(ext)s" {url}')
        return "song.mp3"


class YoutubeMusic(commands.Cog):
    
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.queue = deque()
        
    @commands.command()#
    async def join(self, ctx):
        channel = ctx.author.voice.channel if ctx.author.voice else None

        try:
            if channel is None:
                await ctx.send(f"**{ctx.author.name}** odpierdol sie, jesli nie jestes w czacie glosowym")
                return
            elif not ctx.voice_client:
                await channel.connect()
                ctx.voice_client.stop()
        except Exception as err:
            await ctx.send(f"{err}")
                
        
    @commands.command()
    async def play(self, ctx, *video):
        song = " ".join(video)  
        try:
            await self.join(ctx) 
            async with ctx.typing():
                filename = await YTDLSource.from_url(song, loop=self.bot.loop)
                ctx.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=filename.replace("webm", "mp3") if "webm" in filename else filename.replace("m4a", "mp3")))
            await ctx.send(f"**Teraz napierdalamy** {YTDLSource._get_name(song)}")
        except:
            await ctx.send("Cus sie stanelo")
        
    
    @commands.command()
    async def pause(self, ctx):
        voice = ctx.voice_client if ctx.voice_client else None
        
        if voice is None:
            await ctx.send(f"**{ctx.author.name}** A wyglada Ci kurwa na to zebym byl na czacie?")
            return
        
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("Przeciez nic kurwa nie gram")
            
    @commands.command()
    async def resume(self, ctx):
        voice = ctx.voice_client
        
        if voice.is_paused():
            voice.resume()
            
    @commands.command()
    async def stop(self, ctx):
        voice = ctx.voice_client
        
        if voice.is_playing() or voice.is_paused():
            voice.stop()
    
    @commands.command()
    async def skip(self, ctx):
        voice = ctx.voice_client
        
        voice.stop()
    
    @commands.command()
    async def leave(self, ctx):    
        if not ctx.voice_client:
            await ctx.send(f"{ctx.author.name} :fuckyou:")
        else:
            await ctx.voice_client.disconnect()
            
    @commands.command()
    async def loop(self, ctx):
        voice_client = ctx.voice_client
        if not voice_client:
            await ctx.author.voice.channel.connect()
     
     
def setup(bot: Bot):
    bot.add_cog(YoutubeMusic(bot))