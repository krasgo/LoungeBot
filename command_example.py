import discord
import asyncio
from discord.ext import commands

class ExampleClass:
    def __init__(self, client):
        self.client = client
    
    @commands.command(pass_context=True)
    async def example_cmd(self, ctx):
        await ctx.send('i did it! example_cmd!')

def setup(client):
    client.add_cog(ExampleClass(client))