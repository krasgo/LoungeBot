import discord
import asyncio
from discord.ext import commands

ec_game = None

class ExquisiteCorpse:
    def __init__(self, client):
        self.client = client
        
    @commands.command(pass_context=True)
    async def ec(self, ctx):
        players = ctx.message.mentions
        
        if len(players) != 3:
            await self.client.say('Need three mentions!')
        else:
            await self.client.say('ec working!')
    
    '''
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
                    '''

def setup(client):
    client.add_cog(ExquisiteCorpse(client))