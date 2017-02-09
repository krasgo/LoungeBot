import discord
import asyncio
from discord.ext import commands
import bot_info
from io import StringIO
import sys
import signal
import math
from enum import Enum

class FormatType(Enum):
    MONO = 0
    NORM = 1
    EMBD = 2

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
        
        # Get output
        output = None
        try:
            output = eval(str(cmd_str))
        except TimeoutError as e:
            output = "Timeout!"
        finally:
            signal.alarm(0)

        await self.client.say('```\n' + str(output) + '\n```')
    
    # oh no exec
    @commands.command(description='oh NO!!!! dont do it man!!!\n ' + \
            'begin script with -n for no monospace, -e for embed style')
    @commands.check(bot_info.is_owner)
    async def botexec(self, *, cmd_str : str = None):
        signal.signal(signal.SIGALRM, interrupt)
        signal.alarm(self.timeout_length)
        
        cmd_str = cmd_str.strip()
        
        # By default, text is monospaced with ```
        format_type = FormatType.MONO
        
        # No monospace, no embed, just plain
        if(cmd_str.startswith('-n')):
            format_type = FormatType.NORM
            cmd_str = cmd_str[2:]
        
        # Embed
        if(cmd_str.startswith('-e')):
            format_type = FormatType.EMBD
            cmd_str = cmd_str[2:]
        
        cmd_str = cmd_str.strip()
        
        # Exec and get the output
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        
        try:
            exec(str(cmd_str))
        except TimeoutError as e:
            print("Timeout!")
        finally:
            signal.alarm(0)
            
        sys.stdout = old_stdout
        
        # Print the output
        if(format_type == FormatType.MONO):
            await self.client.say('```\n' + redirected_output.getvalue() + '\n```')
        elif(format_type == FormatType.NORM):
            await self.client.say(redirected_output.getvalue())
        elif(format_type == FormatType.EMBD):
            em = discord.Embed(description=redirected_output.getvalue(), colour=0x32CD32)
            await self.client.say(embed=em)
        
def setup(client):
    client.add_cog(Corruption(client))
