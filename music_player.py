import discord
import asyncio
from discord.ext import commands
import youtube_dl

class MusicPlayer:
    def __init__(self, client):
        self.client = client
        self.voice = None
    
    # Youtube player
    @commands.command(pass_context=True)
    async def play(self, ctx, yt_url : str = None):
        if not yt_url is None:
            try:
                # If already playing something, disconnect to reset
                if not self.voice is None:
                    await self.voice.disconnect()
                    self.voice = None
                
                # Start playing
                self.voice = await self.client.join_voice_channel(ctx.message.author.voice_channel)
                player = await self.voice.create_ytdl_player(yt_url, ytdl_options={'format': 'worst', 'audioformat': 'mp3'})
                player.start()
            except Exception as e:
                await client.send_message(message.channel, 'Err:\n```\n' + str(e) + '```')
        else:
            await self.client.say('Usage: /play youtube_url')
    
    # Disconnect the bot from the voice chat
    @commands.command()
    async def play_leave(self):
        try:
            await self.voice.disconnect()
            self.voice = None
        except Exception as e:
            await self.client.say('Err:\n```\n' + str(e) + '\n```')

def setup(client):
    client.add_cog(MusicPlayer(client))