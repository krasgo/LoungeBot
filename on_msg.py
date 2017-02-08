import discord
import asyncio
from discord.ext import commands
import urllib.request
import youtube_dl
import string
import random
import bot_info
import requests

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

    # Chat survey
    @commands.command(description='Sends a survey to the chat for members " + \
            "to answer. Usage: /survey (-start [question], -end)')
    async def survey(self, *, args_str : str = None):
        try:
            args = args_str.split() if len(args_str) else [""]
            global survey_inst 

            if not survey_inst is None and not survey_inst.running:
                self.client.say("survey_inst == None, not running")
                #survey_inst = None
            if survey_inst is None and len(args) > 0 and args[0] == '-start':
                self.client.say("survey_inst == None, -start")
                #survey_inst = survey.Survey(message)
                #await survey_inst.prompt(message, client)
            elif survey_inst is not None and len(args) > 0 and args[0] == '-end':
                self.client.say("survey_inst running, -end")
                #if survey_inst.surveyor is message.author:
                #    await survey_inst.end(message, client)
                #    survey_inst = None
                #else:
                #    await client.delete_message(message)
                #    await self.client.say( 
                #            "No. Only the user who asked the " + \
                #            "question can end it")
            elif survey_inst is not None and len(args) > 0 and args[1] == '-start':
                self.client.say("survey_inst running, -start")
                #await client.delete_message(message)
                #await client.send_message(message.channel, 
                #        "A question is already being asked.")
            elif survey_inst is not None and len(args) > 0: 
                self.client.say("survey_inst running, response to be received")
                #    await survey_inst.response(message, client)

            else:
                await self.client.say(
                        "Usage:\n\t`/survey -start [question]` to ask a question" + \
                                "\n\t`/survey [response]`  to respond " + \
                                "\n\t`/survey -end` to show results")
        except Exception as e:
            await self.client.say('Err:\n```\n' + str(e) + '```')

def setup(client):
    client.add_cog(General(client))
