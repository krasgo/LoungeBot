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
            
    
    @commands.command(description="Know the future", pass_context=True)
    async def magic8ball(self, ctx, *, question : str = None):
        await ctx.send(random.choice(self.answers))
def setup(client):
    client.add_cog(Magic8Ball(client))