import discord
import asyncio
import urllib.request
import ec

ec_game = None

class Msger:
	def __init__(self, message, client):
		self.message = message
		self.client = client

	async def handle_msg(self):
		message = self.message
		client = self.client
		args = message.content.split()
		
		# Don't check the arguments if there are none
		if len(args) == 0:
			return
		
		# Test the bot
		if args[0] == '/ping':
			await client.send_message(message.channel, 'meow!')

		# Change profile icon
		if args[0] == '/chg_avatar':
			try:
				# Read from URL
				if len(args) == 2:
					a = urllib.request.urlopen(args[1]).read()
					await client.edit_profile(avatar=a)
					await client.send_message(message.channel, 'Avatar changed!')
				# Read from computer hosting the bot
				elif len(args) == 3 and args[1] == 'local':
					with open(args[2], 'rb') as a:
						await client.edit_profile(avatar=(a.read()))
					await client.send_message(message.channel, 'Avatar changed!')
				# You didn't do it right
				else:
					await client.send_message(message.channel, 'usage: /chg_avatar [local] url/file_path')
			except Exception as e:
				error_msg = 'Error:\n```\n' + str(e) + '\n```'
				await client.send_message(message.channel, error_msg)
		
		# Exquisite Corpse
		if args[0] == '/ec':
			global ec_game
			
			# End the game if it was finished
			if not ec_game is None and ec_game.killme == True:
				ec_game = None
				
			# Start the game if you gave 3 users
			if ec_game is None:
				players = message.mentions
				if len(players) == 3:
					ec_game = ec.ECorpse(players[0], players[1], players[2])
					await ec_game.welcome(message, client)
				else:
					await client.send_message(message.channel, 'I want three players!')
			else:
				# End the game if it was started
				if len(args) == 2 and args[1] == 'end':
					await client.send_message(message.channel, 'Game ended!')
					ec_game = None
				# Allow people to input answers
				else:
					await ec_game.input_answer(message, client, message.author)

		# Clears the chat
		if args[0] == '/clear':
			await client.send_message(message.channel, '.' + '\n' * 100 + '.')

		# Removes your message (testing purposes)
		if args[0] == '/remove':
			await client.delete_message(message)
