import discord
import asyncio
from discord.ext import commands
import importlib
import bot_info
import sys

extensions = ['general', 'survey', 'music_player', 'games', 'git', 'corruption', 'translate', 'magic8ball']
bot = commands.Bot(command_prefix=commands.when_mentioned_or('/'), description='Here you go! All my commands!')

# Loads extensions, returns string saying what reloaded
def reload_extensions(exs):
    module_msg = ''
    for ex in exs:
        try:
            bot.unload_extension(ex)
            bot.load_extension(ex)
            module_msg += 'module "{}" reloaded\n'.format(ex)
        except Exception as e:
            module_msg += 'reloading "{}" failed, error is:```{}```\n'.format(ex, e)
    return module_msg

    
    
    
    
# Set up stuff
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    #await bot.change_presence(game=discord.Game(name='Dreams Beta'))
    print(reload_extensions(extensions))

# Process commands
@bot.event
async def on_message(message):
    await bot.process_commands(message)

# Command error
@bot.event
async def on_command_error(ctx, error):
    await ctx.send('Oops, something is wrong!\n```\n' + repr(error) + '\n```')
    
# Reloading extensions
@bot.command(description='Reloads extensions. Usage: /reload [extension_list]', pass_context=True)
@bot_info.is_owner()
async def reload(ctx, *, exs : str = None):
    module_msg = 'd' # d
    if(exs is None):
        module_msg = reload_extensions(extensions)
    else:
        module_msg = reload_extensions(exs.split())
    await ctx.send(module_msg)

for ex in extensions:
    try:
        bot.load_extension(ex)
    except Exception as e:
        print('Failed to load {} because: {}'.format(ex, e))

# Start the bot
bot.run(bot_info.data['login'])
