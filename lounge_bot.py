import discord
import asyncio
from discord.ext import commands
import importlib
import bot_info
import sys
import command_example

extensions = ['on_msg', 'ec', 'survey', 'command_example', 'music_player']
client = commands.Bot(command_prefix='/', description='Here you go! All my commands!')

# Loads extensions, returns string saying what reloaded
def reload_extensions(exs):
    module_msg = ''
    for ex in exs:
        try:
            client.unload_extension(ex)
            client.load_extension(ex)
            module_msg += 'module "{}" reloaded\n'.format(ex)
        except Exception as e:
            module_msg += 'reloading "{}" failed, error is:```{}```\n'.format(ex, e)
    return module_msg

    
    
    
    
# Set up stuff
@client.async_event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    yield from client.change_presence(game=discord.Game(name='Dreams Beta'))
    print(reload_extensions(extensions))

# Process commands
@client.event
async def on_message(message):
    await client.process_commands(message)

# Command error
@client.event
async def on_command_error(error, context):
    await client.send_message(context.message.channel, 'Oops, something is wrong!\n```\n' + repr(error) + '\n```')
    
# Reloading extensions
@client.command(description='Reloads extensions. Usage: /reload [extension_list]')
@commands.check(bot_info.is_owner)
async def reload(*, exs : str = None):
    module_msg = 'd' # d
    if(exs is None):
        module_msg = reload_extensions(extensions)
    else:
        module_msg = reload_extensions(exs.split())
    await client.say(module_msg)

# Start the bot
client.run(bot_info.data['login'])
