import discord
import asyncio
from discord.ext import commands
import urllib.request
import youtube_dl
import string
import random
import bot_info
import requests
from io import StringIO
import sys

ec_game = None
survey_inst = None

class General:
    def __init__(self, client):
        self.client = client
        
    # Ping!
    @commands.command(description='ping!')
    async def ping(self):
        await self.client.say('coucou !')
        
    # Change profile icon
    @commands.command(description='Changes the avatar. Usage: /chg_avatar (local | url) path')
    async def chg_avatar(self, path_type : str = None, *, path : str = None):
        if (path_type == 'url' or path_type == 'local') and not path is None:
            try:
                # URL
                if path_type == 'url':
                    a = urllib.request.urlopen(path).read()
                    await self.client.edit_profile(avatar=a)
                    await self.client.say('Avatar changed!')
                # Local
                elif path_type == 'local':
                    with open(path, 'rb') as a:
                        await self.client.edit_profile(avatar=(a.read()))
                    await self.client.say('Avatar changed!')
            except Exception as e:
                await self.client.say('Error:\n```\n' + str(e) + '\n```')
        else:
            await self.client.say('Usage: /chg_avatar (local | url) path')
    
    # Clear
    @commands.command(description='Clears the chat')
    async def clear(self):
        await self.client.say('.' + '\n' * 100 + '.')
    
    # Random imgur links
    @commands.command(description='Get random imgur links. Usage: /imgur [amount]')
    async def imgur(self, amount : int = 1):
        try:
            imgur_host = 'http://i.imgur.com/'
            imgur_suffix = '.png'
            
            max_attempts = 20
            img_url_len = 5
            
            msg_urls = ''
            
            # Check the number of attempts requested
            if amount > max_attempts:
                amount = max_attempts
                msg_urls += 'Sorry man, only ' + max_attempts + ' links allowed (nik doesn\'t want you stressing out his pi like that)\n'
            elif amount < 1:
                amount = 1
            
            await self.client.say('Loading...')
            
            # Get the requested number of links
            i = 0
            while i < amount:
                imgur_path = imgur_host
                for j in range(img_url_len):
                    imgur_path += random.choice(string.ascii_letters + string.digits)
                imgur_path += imgur_suffix
                r = requests.get(imgur_path)
                
                if len(r.history) is 0:
                    msg_urls += str(imgur_path) + '\n'
                else:
                    amount += 1
                i += 1
                r.history = []
            await self.client.say(msg_urls)
        except Exception as e:
            await self.client.say('Err:\n```\n' + str(e) + '```')

def setup(client):
    client.add_cog(General(client))
