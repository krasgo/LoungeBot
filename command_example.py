import discord
import asyncio
from discord.ext import commands

class ExampleClass:
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def example_cmd(self):
        await self.client.say('i did it! example_cmd!')

def setup(client):
    client.add_cog(ExampleClass(client))