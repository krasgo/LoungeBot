import discord
import asyncio
from random import shuffle

class ECorpse:
    def __init__(self, user0, user1, user2):
        self.users = [user0, user1, user2]
        shuffle(self.users)
        
        # Signals end game
        self.killme = False
        # Dictionary of all the answers
        self.answers = { self.users[0]: None, self.users[1]: None, self.users[2]: None }
    
    async def welcome(self, message, client):
        welcome_message = 'Game started!\n' + '-' * 25 + \
                        '\n**Noun:** ' + self.users[0].mention + \
                        '\n**Verb:** ' + self.users[1].mention + \
                        '\n**Reason:** ' + self.users[2].mention + \
                        '\n' + '-' * 25 + '\nTo enter an answer, type `/ec your answer`'
        await client.send_message(message.channel, welcome_message)
    
    async def input_answer(self, message, client, user):
        if user in self.answers:
            # Record an answer
            if self.answers[user] is None:
                self.answers[user] = message.content[4:]
                await client.delete_message(message)
                await client.send_message(message.channel, user.mention + ' has submitted their answer!')
            # Say they already recorded an answer
            else:
                await client.send_message(message.channel, 'You already gave an answer')
        else:
            await client.send_message(message.channel, "You're not playing")
        
        # Check if all answers were given
        all_answered = True
        for k, v in self.answers.items():
            if v is None:
                all_answered = False
                break
        if all_answered:
            end_message = 'All answers given! The results are:\n' + '-' * 25 + '\n```\n'
            end_message += self.answers[self.users[0]] + '\n'
            end_message += self.answers[self.users[1]] + '\n'
            end_message += self.answers[self.users[2]] + '```\n'
            killme = True
            await client.send_message(message.channel, end_message)