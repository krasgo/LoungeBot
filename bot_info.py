import json

# Load bot info (contains login and owners)
data = None
with open('bot_info.json') as f:
    data = json.load(f)

# Returns true if you're privileged
def is_owner(ctx):
    return ctx.message.author.id in data['owners']

def get_yandex_translate_key():
    return data['yandex-translate']