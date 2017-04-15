import discord
from discord.ext import commands
import asyncio
import random

class Magic8Ball:
    def __init__(self, client):
        self.client = client
        self.answers=['Nope.',
            'Yep.',
            'Maybe some day',
            'Ask again',
            'As likely as Elena showing us her clop blog',
            'hecc no',
            'ye',
            'Try asking again',
            'heck YEAH']
            
    
    @commands.command(description="Know the future")
    async def magic8ball(self, *, question : str = None):
        await self.client.say(random.choice(self.answers))
def setup(client):
    client.add_cog(Magic8Ball(client))