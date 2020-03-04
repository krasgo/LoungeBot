import discord
from discord.ext import commands
import asyncio
import random

class Magic8Ball(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.answers=['Nope.',
            'Yep.',
            'Maybe some day',
            'Ask again',
            'hecc no',
            'ye',
            'Try asking again',
            'heck YEAH',
            "LOL no",
            "AWW YEAAAHHHH"]
            
    
    @commands.command(description="Know the future", pass_context=True)
    async def magic8ball(self, ctx, *, question : str = None):
        await ctx.send(random.choice(self.answers))
def setup(bot):
    bot.add_cog(Magic8Ball(bot))