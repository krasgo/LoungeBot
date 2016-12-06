import discord
import asyncio

start_len = "/survey -start ".len() 
resp_len = "/survey ".len()
class Survey:
    def __init__(self, message):
        self.running = True
        self.surveyor = message.author
        self.member_answered = {member:False for member 
                in message.server.members}
        self.answers = []

    async def prompt(self, message, client):
        await client.delete_message(message)
        msg = "A user has submitted a question:```\n" + \
                message.content[start_len:] + \
                "```\nAnswer this question anonymously by typing" + \
                " `/survey` before your response."
        await client.send_message(message.channel, msg)

    async def response(self, message, client):
        if not self.member_answered[message.author]:
            self.answers.append(message.content[resp_len:])
            await client.delete_message(message)
            self.member_answered[message.author] = True
            await client.send_message(message.channel, "Response submitted.")
        else: 
            await client.delete_message(message)
            await client.send_message(message.channel, 
                    "You've already submitted a response, " + message.author.mention)

    async def end(self, message, client):
        ans = [x + "\n\n" for x in self.answers]
        await client.delete_message(message)
        msg = "The user has closed the question. Here are the responses:\n" + \
              '```\n' + "".join(ans) + '```'
        self.running = False
        await client.send_message(message.channel, msg)
        
