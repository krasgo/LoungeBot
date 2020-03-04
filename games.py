import discord
import asyncio
from discord.ext import commands

ec_game = None

class ExquisiteCorpse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(pass_context=True)
    async def ec(self, ctx):
        ctx.send("Feature not yet implemented :(")
        return
        players = ctx.message.mentions
        
        if len(players) != 3:
            await ctx.send('Need three mentions!')
        else:
            await ctx.send('ec working!')
    
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
                    await ec_game.welcome(message, bot)
                else:
                    await bot.send_message(message.channel, 'I want three players!')
            else:
                # End the game if it was started
                if len(args) == 2 and args[1] == 'end':
                    await bot.send_message(message.channel, 'Game ended!')
                    ec_game = None
                # Allow people to input answers
                else:
                    await ec_game.input_answer(message, bot, message.author)
                    '''

def setup(bot):
    bot.add_cog(ExquisiteCorpse(bot))