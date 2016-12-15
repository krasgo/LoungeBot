import discord
import asyncio
from discord.ext import commands
import urllib.request
import subprocess
from subprocess import Popen
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
        await self.client.say('miaou!')
    
    # Do git pull
    @commands.command(description='Runs "git pull" on the computer I\'m running on')
    @commands.check(bot_info.is_owner)
    async def pull(self):
        try:
            p = Popen(['git', 'pull'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
                
            await self.client.say('Ran git pull!')
        except Exception as e:
            await self.client.say('Error:\n```\n' + str(e) + '```')
        
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
'''    
    async def handle_msg(self):
        # Exquisite Corpse
        if args[0] == '/ec':
            global ec_game
            
            # End the game if it was finished
            if not ec_game is None and ec_game.killme == True:
                ec_game = None
                
            # Start the game if you gave 3 users
            if ec_game is None:
                players = message.mentions
                if len(players) == 3:
                    ec_game = ec.ECorpse(players[0], players[1], players[2])
                    await ec_game.welcome(message, client)
                else:
                    await client.send_message(message.channel, 'I want three players!')
            else:
                # End the game if it was started
                if len(args) == 2 and args[1] == 'end':
                    await client.send_message(message.channel, 'Game ended!')
                    ec_game = None
                # Allow people to input answers
                else:
                    await ec_game.input_answer(message, client, message.author)

        # Survey
        if args[0] == '/survey':
            try:
                global survey_inst
                
                if not survey_inst is None and not survey_inst.running:
                    survey_inst = None

                if survey_inst is None and len(args) > 1 and args[1] == '-start':
                    survey_inst = survey.Survey(message)
                    await survey_inst.prompt(message, client)
                elif survey_inst is not None and len(args) > 1 and args[1] == '-end':
                    if survey_inst.surveyor is message.author:
                        await survey_inst.end(message, client)
                        survey_inst = None
                    else:
                        await client.delete_message(message)
                        await client.send_message(message.channel,
                                "No. Only the user who asked the " + \
                                "question can end it")
                elif survey_inst is not None and len(args) > 1 and args[1] == '-start':
                    await client.delete_message(message)
                    await client.send_message(message.channel, 
                            "A question is already being asked.")
                elif survey_inst is not None and len(args) > 1: 
                        await survey_inst.response(message, client)

                else:
                    await client.send_message(message.channel, 
                            "Usage:\n\t`/survey -start [question]` to ask a question" + \
                                    "\n\t`/survey [response]`  to respond " + \
                                    "\n\t`/survey -end` to show results")
            except Exception as e:
                err_msg = 'Err:\n```\n'
                err_msg += str(e) + '```'
                await client.send_message(message.channel, err_msg)
        
        # Gets a random imgur link (that hopefully works)
        if args[0] == '/imgur':
            try:
                imgur_host = "http://i.imgur.com/"
                imgur_suffix = '.png'
                
                max_attempts = 20
                img_url_len = 5 if args[0] == '/imgur' else 6
                
                msg_urls = ''
                
                # Check the number of attempts requested
                attempts = 1
                if len(args) > 1 and int(args[1]) > 1:
                    attempts = int(args[1])
                    if attempts > max_attempts:
                        attempts = max_attempts
                        msg_urls += 'Sorry man, only ' + max_attempts + ' links allowed (nik doesn\'t want you stressing out his pi like that)\n'
                
                await client.send_message(message.channel, 'Loading...')
                
                # Get that number of links
                i = 0
                while i < attempts:
                    imgur_path = imgur_host 
                    for j in range(img_url_len):
                        imgur_path += random.choice(string.ascii_letters + string.digits)
                    imgur_path += imgur_suffix
                    r = requests.get(imgur_path)
                    
                    if len(r.history) is 0:
                        msg_urls += str(imgur_path) + '\n'
                    else:
                        attempts += 1
                    i += 1
                    r.history = []
                await client.send_message(message.channel, msg_urls)
            except Exception as e:
                err_msg = 'Err:\n```\n' + str(e) + '```'
                await client.send_message(message.channel, err_msg)

        if args[0] == '/pretend':
            try:
                await client.delete_message(message)
                class pt:
                    member = message.mentions[0]
                    name = member.display_name
                    colour = member.colour
                    msg_len = len('/pretend   <>' + member.id)
                    msg = message.content[msg_len:]
                class bot:
                    name = client.user.display_name
                    member = message.server.me
                    colour = message.server.me.colour
                    role = message.server.me.top_role
                
                await client.change_nickname(bot.member, pt.name)
                await client.send_message(message.channel, pt.msg)
                await client.change_nickname(bot.member, bot.name)

            except Exception as e:
                err_msg = 'Err:\n```\n' + str(e) + '```'
                await client.send_message(message.channel, err_msg)

        if args[0] == '/gimg':
            word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
            response = requests.get(word_site)
            WORDS = response.content.splitlines()
            await client.send_message(message.channel, random.choice(WORDS))
                
        # Removes your message (testing purposes)
        if args[0] == '/remove':
            await client.delete_message(message)
'''