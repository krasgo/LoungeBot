import discord
import asyncio
from discord.ext import commands
import bot_info
from io import StringIO
import sys
import signal
import math

class TimeoutError(Exception):
    pass

def interrupt():
    raise TimeoutError()
        
class Corruption:
    def __init__(self, client):
        self.client = client
        self.timeout_length = 10
    
    # Eval!
    @commands.command(description='Use with care please')
    async def eval(self, *, cmd_str : str = None):
        signal.signal(signal.SIGALRM, interrupt)
        signal.alarm(self.timeout_length) 
        
        output = None
        try:
            output = eval(str(cmd_str))
        except TimeoutError as e:
            output = "Timeout!"
        finally:
            signal.alarm(0)

        await self.client.say('```\n' + str(output) + '\n```')
    
    # oh no exec
    @commands.command(description='oh NO!!!! dont do it man!!!')
    @commands.check(bot_info.is_owner)
    async def botexec(self, *, cmd_str : str = None):
        signal.signal(signal.SIGALRM, interrupt)
        signal.alarm(self.timeout_length) 
        
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        
        try:
            exec(str(cmd_str))
        except TimeoutError as e:
            print("Timeout!")
        finally:
            signal.alarm(0)
            
        sys.stdout = old_stdout
        
        await self.client.say('```\n' + redirected_output.getvalue() + '\n```')
        
def setup(client):
    client.add_cog(Corruption(client))
