import discord
import asyncio
import importlib
import json
import sys
import on_msg

# Load bot info (contains login and owners)
bot_info = None
with open('bot_info.json') as f:
	bot_info = json.load(f)

client = discord.Client()

@client.async_event
def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	yield from client.change_presence(game=discord.Game(name='Dreams Beta'))

@client.event
async def on_message(message):
	# Reload the modules
	if message.author.id in bot_info['owners'] and message.content.startswith('/reload'):
		# Reload only select modules
		arg_len = len(message.content.split())
		if arg_len > 1:
			module_msg = ''
			for i in range(1, arg_len):
				try:
					importlib.reload(sys.modules[message.content.split()[i]])
					module_msg += 'module "{}" reloaded\n'.format(message.content.split()[i])
				except Exception as e:
					module_msg += 'reloading "{}" failed, error is:```{}```\n'.format(message.content.split()[i], e)
			await client.send_message(message.channel, module_msg)
		else:
			module_list = ['ec', 'on_msg', 'survey']
			module_msg = ''
			for i in module_list:
				try:
					importlib.reload(sys.modules[i])
					module_msg += 'module "{}" reloaded\n'.format(i)
				except Exception as e:
					module_msg += 'reloading "{}" failed, error is:```{}```\n'.format(i, e)
			await client.send_message(message.channel, module_msg)
	await on_msg.Msger(message, client).handle_msg()

client.run(bot_info['login'])
