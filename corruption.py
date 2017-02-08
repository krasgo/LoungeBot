import discord
import asyncio
from discord.ext import commands
import bot_info
from io import StringIO
import sys

class Corruption:
    def __init__(self, client):
        self.client = client

    # Eval!
    @commands.command(description='Use with care please')
    async def eval(self, *, cmd_str : str = None):
        output = eval(str(cmd_str))
        await self.client.say('```\n' + str(output) + '\n```')
    
    # oh no exec
    @commands.command(description='oh NO!!!! dont do it man!!!')
    @commands.check(bot_info.is_owner)
    async def botexec(self, *, cmd_str : str = None):
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        exec(str(cmd_str))
        sys.stdout = old_stdout
        
        await self.client.say('```\n' + redirected_output.getvalue() + '\n```')
        
def setup(client):
    client.add_cog(Corruption(client))