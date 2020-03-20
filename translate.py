import discord
from discord.ext import commands
import asyncio
import bot_info
import requests
import random

class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.key = bot_info.get_yandex_translate_key()
        self.langs = ['ar',
            'be', 
            'cy', 
            'el', 
            'da', 
            'he', 
            'ga', 
            'it', 
            'es', 
            'kk', 
            'la', 
            'mt', 
            'de', 
            'no', 
            'fa', 
            'pl', 
            'ru', 
            'sk', 
            'tr', 
            'uk', 
            'fi', 
            'fr', 
            'sv', 
            'eo', 
            'ja']
        self.langs_friendly = ['Arabic',
            'Belarusian',
            'Welsh',
            'Greek',
            'Danish',
            'Hebrew',
            'Irish',
            'Italian',
            'Spanish',
            'Kazakh',
            'Latin',
            'Maltese',
            'German',
            'Norwegian',
            'Persian',
            'Polish',
            'Russian',
            'Slovakian',
            'Turkish',
            'Ukrainian',
            'Finnish',
            'French',
            'Swedish',
            'Esperanto',
            'Japanese']
            
    @commands.command(description="Translate to English", pass_context=True)
    async def translate(self, ctx, *, lang_input : str = None):
        yandex_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
        yandex_url += '?key=' + self.key
        yandex_url += '&text=' + lang_input
        yandex_url += '&lang=en'
        r = requests.get(yandex_url)
        translation = r.json()['text']
        await ctx.send(translation[0])
    
    @commands.command(description="Translate back and forth", pass_context=True)
    async def translatemix(self, ctx, amount : int, *, english : str = None):
        translation = english
        trans_history = '__Translations:__\n'
        
        if amount < 1:
            amount = 1
        if amount > 20:
            amount = 20
        
        await ctx.send("Loading...")
        used_langs = []
        prev_lang_i = -1
        lang_i = -1
        for i in range(amount):
            while(prev_lang_i == lang_i or lang_i in used_langs):
                lang_i = random.choice(range(len(self.langs)))
            lang = self.langs[lang_i]
            prev_lang = -1 if prev_lang_i == -1 else self.langs[prev_lang_i]
            used_langs.append(lang_i)
            
            yandex_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
            yandex_url += '?key=' + self.key
            yandex_url += '&text=' + translation
            if prev_lang_i == -1:
                yandex_url += '&lang=' + lang
            else:
                yandex_url += '&lang=' + prev_lang + '-' + lang
            r = requests.get(yandex_url)
            translation = r.json()['text'][0]
            trans_history += '**{}**: {}\n'.format(self.langs_friendly[lang_i], translation)
            prev_lang_i = lang_i
            
        yandex_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
        yandex_url += '?key=' + self.key
        yandex_url += '&text=' + translation
        yandex_url += '&lang=en'
        r = requests.get(yandex_url)
        translation = r.json()['text'][0]
        #final_part = '\n__Final translation to English:__\n**{}**'.format(translation)
        final_msg = '\n__Final translation to English:__\n**{}**'.format(translation)
        #if len(trans_history + final_msg) >= 2000:
        #    used_langs_str = ' -> '.join(map(lambda i: self.langs_friendly[i], used_langs))
        #    trans_history = used_langs_str + ' -> English\n{}'.format(final_msg)
        #else:
        #    trans_history += final_msg
        trans_history += final_msg

        if len(trans_history) > 2000:
                #for i in range(0, len(trans_history), 2000):
                #await ctx.send(trans_history[i:min(len(trans_history), i+2000)])
                ctx.send(trans_history[0:2000])
        else:
            await ctx.send(trans_history)

def setup(bot):
    bot.add_cog(Translate(bot))
