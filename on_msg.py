import discord
import asyncio
import urllib.request
import subprocess
from subprocess import Popen
import youtube_dl
import string
import random
import json
import ec
import survey
import requests

ec_game = None
survey_inst = None

class Msger:
    def __init__(self, message, client):
        self.message = message
        self.client = client

    async def handle_msg(self):
        message = self.message
        client = self.client
        args = message.content.split()
        
        # Don't check the arguments if there are none
        if len(args) == 0:
            return
        
        # Test the bot
        if args[0] == '/ping':
            await client.send_message(message.channel, 'miaou !')
        
        bot_info = None
        with open('bot_info.json') as f:
            bot_info = json.load(f)
        # Do git pull
        if args[0] == '/pull' and message.author.id in bot_info['owners']:
            try:
                p = Popen(['git', 'pull'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
                
                await client.send_message(message.channel, 'Ran git pull!')
            except Exception as e:
                await client.send_message(message.channel, 'Error:\n```\n' + str(e) + '```')

        # Change profile icon
        if args[0] == '/chg_avatar':
            try:
                # Read from URL
                if len(args) == 2:
                    a = urllib.request.urlopen(args[1]).read()
                    await client.edit_profile(avatar=a)
                    await client.send_message(message.channel, 'Avatar changed!')
                # Read from computer hosting the bot
                elif len(args) == 3 and args[1] == 'local':
                    with open(args[2], 'rb') as a:
                        await client.edit_profile(avatar=(a.read()))
                    await client.send_message(message.channel, 'Avatar changed!')
                # You didn't do it right
                else:
                    await client.send_message(message.channel, 'usage: /chg_avatar [local] url/file_path')
            except Exception as e:
                error_msg = 'Error:\n```\n' + str(e) + '\n```'
                await client.send_message(message.channel, error_msg)
        
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

        # Clears the chat
        if args[0] == '/clear':
            await client.send_message(message.channel, '.' + '\n' * 100 + '.')

        # Youtube player
        if args[0] == '/play':
            try:
                if len(args) > 1:
                    voice = await client.join_voice_channel(message.author.voice_channel)
                    player = await voice.create_ytdl_player(args[1])
                    player.start()
                else:
                    await client.send_message(message.channel, "Please enter a URL after the `/play` command")
            except Exception as e:
                err_msg = 'Err:\n```\n' + str(e) + '```'
                await client.send_message(message.channel, err_msg)
        
        # Gets a random imgur link (that hopefully works)
        if args[0] == '/imgur':
            try:
                imgur_host = "http://i.imgur.com/"
                imgur_suffix = '.png'
                attempts = 1

                http_code = ''

                if len(args) > 1 and int(args[1]) > 1:
                    attempts = int(args[1])
                    if attempts > 5:
                        attempts = 5

                for i in range(attempts):
                    imgur_path = imgur_host 
                    for i in range(5): # 5 since that's how long the end of the url is (well it's 7 now but 5 is more reliable)
                        imgur_path += random.choice(string.ascii_letters + string.digits)
                imgur_path += imgur_suffix
                r = requests.get(imgur_path)
                await client.send_message(message.channel, str(imgur_path) + ", " + str(r.status_code))
            except Exception as e:
                err_msg = 'Err:\n```\n' + str(e) + '```'
                await client.send_message(message.channel, err_msg)

        # Removes your message (testing purposes)
        if args[0] == '/remove':
            await client.delete_message(message)
