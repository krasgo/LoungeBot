import discord
import asyncio
from discord.ext import commands
import subprocess
from subprocess import Popen
import bot_info

class Git(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Do git pull
    # Should only be used by someone who is working on the bot!
    @commands.command(description='Runs "git pull" on the computer I\'m running on', pass_context=True)
    @bot_info.is_owner()
    async def pull(self, ctx):
        try:
            p = Popen(['git', 'pull'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
                
            await ctx.send('Ran git pull!')
        except Exception as e:
            await ctx.send('Error:\n```\n' + str(e) + '```')
    
def setup(bot):
    bot.add_cog(Git(bot))