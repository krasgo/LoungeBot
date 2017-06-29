import discord
from discord.ext import commands
import asyncio

start_len = len("/survey -start ")
resp_len = len("/survey ")

class Survey:
    def __init__(self, client):
        self.client = client
        self.running = False
        self.member_answered = None
        self.answers = []

    @commands.command(description='prompt me, respond, or end me', pass_context=True)
    async def survey(self, ctx, cmd, *, msg : str = None):
        # Asking!
        if cmd == 'prompt':
            if not (msg is None) and not self.running:
                await self.client.delete_message(ctx.message)
                self.running = True
                self.member_answered = {member:False for member 
                    in ctx.message.server.members}
                bot_msg = "A user has submitted a question:```\n" + \
                    msg + \
                    "```\nAnswer this question anonymously by typing" + \
                    " `/survey respond` before your response."
                await ctx.send(bot_msg)
            else:
                if self.running:
                    await ctx.send('A survey is already running!')
                else:
                    await ctx.send('You must ask a question')
        # Responding!
        elif cmd == 'respond':
            if not (msg is None) and self.running:
                if not self.member_answered[ctx.message.author]:
                    self.answers.append(msg)
                    await self.client.delete_message(ctx.message)
                    self.member_answered[ctx.message.author] = True
                    await ctx.send("Response submitted.")
                else: 
                    await self.client.delete_message(ctx.message)
                    await ctx.send("You've already submitted a response, " + ctx.message.author.mention)
            else:
                if self.running:
                    await ctx.send('You gotta answer the question lmafo')
                else:
                    await ctx.send('Nothing to respond to, start a survey with `/survey prompt`!')
        # End me!
        elif cmd == 'end':
            if self.running:
                ans = [x + "\n\n" for x in self.answers]
                await self.client.delete_message(ctx.message)
                bot_msg = "The user has closed the question. Here are the responses:\n" + \
                      '```\n' + "".join(ans) + '```'
                self.running = False
                await ctx.send(bot_msg)
            else:
                await ctx.send('Nothing to end, start a survey with `/survey prompt`!')
        else:
            await ctx.send('Invalid command, use `/survey prompt`, `/survey respond`, or `/survey end`')

def setup(client):
    client.add_cog(Survey(client))