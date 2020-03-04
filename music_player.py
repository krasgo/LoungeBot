import discord
import asyncio
from discord.ext import commands
import youtube_dl

class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice = None
    
    # Youtube player
    @commands.command(pass_context=True)
    async def play(self, ctx, yt_url : str = None):
        # Oh no, this doesn't work yet... Fix later
        await ctx.send("Not yet implemented...")
        return

        if not yt_url is None:
            # If already playing something, disconnect to reset
            if not self.voice is None:
                await self.voice.disconnect()
                self.voice = None
            
            # Start playing
            self.voice = await self.bot.join_voice_channel(ctx.message.author.voice_channel)
            player = await self.voice.create_ytdl_player(yt_url)
            player.start()
        else:
            await ctx.send('Usage: /play youtube_url')
    
    # Disconnect the bot from the voice chat
    @commands.command(pass_context=True)
    async def play_leave(self, ctx):
        # Oh no, this doesn't work yet... Fix later
        await ctx.send("Not yet implemented...")
        return

        try:
            await self.voice.disconnect()
            self.voice = None
        except Exception as e:
            await ctx.send('Err:\n```\n' + str(e) + '\n```')

def setup(bot):
    bot.add_cog(MusicPlayer(bot))