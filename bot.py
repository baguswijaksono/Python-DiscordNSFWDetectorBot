import re
from urllib.request import urlopen
import requests
import aiohttp
from discord.ext import commands
import json
from signal import default_int_handler
from requests import delete, options
import asyncio
import discord
import os

class NudeityDetector(commands.Bot): 
        def _init_(self, commands_prefix, **options):
            super()._init_(commands_prefix, **options)
            self.deepai_key = "yourownapikey"
            self.deepai_key_url= "https://api.deepai.org/api/nsfw-detector'"

        async def deteksi_telanjang(self, link):
            async with aiohttp.ClientSession() as session:
                self.deepai_key = "478cd374-ce66-4fcd-a1f9-b96527f62085"
                self.deepai_key_url= "https://api.deepai.org/api/nsfw-detector"
                async with session.post(self.deepai_key_url, data={'image':link}, headers={'api-key':self.deepai_key}) as response:
                    hasil=await response.json()
                    print(hasil)
                    indeks_ketelanjangan=hasil['output']['nsfw_score']
                    if indeks_ketelanjangan>0.50:
                        return True
                    else:
                        return False   

        async def on_message(self, message):
            URL_REGEX = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
            urls=re.findall(URL_REGEX, message.content)
            links= [link.strip("<>") for link in urls] + [file.url for file in message.attachments]
            for link in links:
                is_nude = await self.deteksi_telanjang(link)
                x=str(message.author)
                if is_nude:
                    await message.delete()
                    embed=discord.Embed(
                    colour= discord.Colour.red()
                    )
                    embed.add_field(name="NSFW Content Detected !",value="Content that " +x+ " send has been removed.", inline=True)
                    await message.channel.send(embed=embed)
                    break

bot = NudeityDetector(command_prefix="!")
bot.run("Yourownbottoken")





