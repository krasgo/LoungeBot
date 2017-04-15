import discord
from discord.ext import commands
import asyncio
import bot_info
import requests
import random

class Translate:
    def __init__(self, client):
        self.client = client
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
            
    @commands.command(description="Translate to something")
    async def translate(self, *, lang_input : str = None):
        yandex_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
        yandex_url += '?key=' + self.key
        yandex_url += '&text=' + lang_input
        yandex_url += '&lang=en'
        r = requests.get(yandex_url)
        translation = r.json()['text']
        await self.client.say(translation[0])
    
    @commands.command(description="Translate back and forth")
    async def transwitch(self, amount : int, *, english : str = None):
        translation = english
        trans_history = ''
        
        if amount < 1:
            amount = 1
        if amount > 20:
            amount = 20
        
        await self.client.say("Loading...")
            
        for i in range(amount):
            lang_i = random.choice(range(len(self.langs)))
            lang = self.langs[lang_i]
            trans_history += self.langs_friendly[lang_i] + ' '
            
            yandex_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
            yandex_url += '?key=' + self.key
            yandex_url += '&text=' + translation
            yandex_url += '&lang=' + lang
            r = requests.get(yandex_url)
            translation = r.json()['text'][0]
            
        yandex_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
        yandex_url += '?key=' + self.key
        yandex_url += '&text=' + translation
        yandex_url += '&lang=en'
        r = requests.get(yandex_url)
        translation = r.json()['text'][0]
        
        await self.client.say('**' + translation + '**\nTranslation order: ' + trans_history + 'English')

def setup(client):
    client.add_cog(Translate(client))