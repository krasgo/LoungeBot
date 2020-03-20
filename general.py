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

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # Ping!
    @commands.command(description='ping!', pass_context=True)
    async def ping(self, ctx):
        await ctx.send('coucou !')
        
    # Change profile icon
    @commands.command(description='Changes the avatar. Usage: /chg_avatar (local | url) path', pass_context=True)
    @bot_info.is_owner()
    async def chg_avatar(self, ctx, path_type : str = None, *, path : str = None):
        if (path_type == 'url' or path_type == 'local') and not path is None:
            try:
                # URL
                if path_type == 'url':
                    a = urllib.request.urlopen(path).read()
                    await self.bot.edit_profile(avatar=a)
                    await ctx.send('Avatar changed!')
                # Local
                elif path_type == 'local':
                    with open(path, 'rb') as a:
                        await self.bot.edit_profile(avatar=(a.read()))
                    await ctx.send('Avatar changed!')
            except Exception as e:
                await ctx.send('Error:\n```\n' + str(e) + '\n```')
        else:
            await ctx.send('Usage: /chg_avatar (local | url) path')
    
    # Clear
    @commands.command(description='Clears the chat', pass_context=True)
    async def clear(self, ctx):
        await ctx.send('.' + '\n' * 100 + '.')
    
    # Random imgur links
    @commands.command(description='Get random imgur links. Usage: /imgur [amount]', pass_context=True)
    async def imgur(self, ctx, amount : int = 1):
        try:
            imgur_host = 'http://i.imgur.com/'
            imgur_suffix = '.png'
            
            max_attempts = 5
            img_url_len = 5
            
            msg_urls = ''
            
            # Check the number of attempts requested
            if amount > max_attempts:
                amount = max_attempts
                msg_urls += 'Sorry man, only ' + str(max_attempts) + ' links allowed (nik doesn\'t want you stressing out his pi like that)\n'
            elif amount < 1:
                amount = 1
            
            await ctx.send('Loading...')
            
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
            await ctx.send(msg_urls)
        except Exception as e:
            await ctx.send('Err:\n```\n' + str(e) + '```')

def setup(bot):
    bot.add_cog(General(bot))
