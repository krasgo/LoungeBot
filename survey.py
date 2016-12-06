import discord
import asyncio

class Survey:
    arg_len = 8

    def __init__(self, message):
        self.running = True
        self.surveyor = message.author
        self.member_answered = {member:False for member 
                in message.server.members}
        self.answers = []

    async def prompt(self, message, client):
        await client.delete_message(message)
        msg = "A user has submitted a question:\n" + \
                message.content[arg_len:] + \
                "\nAnswer this question anonymously by typing" + \
                " `/survey` before your response."
        await client.send_message(message.channel, msg)

    async def response(self, message, client):
        if not self.member_answered[message.author]:
            self.answers += message.content[arg_len:]
            await client.delete_message(message)
            self.member_answered[message.author] = True
            await client.send_message(message.channel, "Response submitted.")
        else:
            await client.send_message(message.channel, 
                    "You've already submitted a response, " + message.author.mention)

    async def end(self, message, client):
        msg = "The user has closed the question. Here are the responses:\n" + \
                "\n".join(self.answers) + "\n"
        self.running = False
        await client.send_message(message.channel, msg)
        
