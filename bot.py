import discord
import datetime
from discord.ext import commands
import os


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

for cog in os.listdir("cogs"):
    try:
        if cog == '__pycache__':
            continue

        else:
            newCog = cog.replace(".py", "")
            bot.load_extension(f"cogs.{newCog}")
            print(f'{cog} successfully loaded!')

    except Exception as e:
        exc = f'{type(e).__name__}: {e}'
        print(f'Failed to load extension {cog}\n{exc}')



class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        #print('Message from {0.author}: {0.content}'.format(message))

        channel = message.channel

        if(message.content == 'hello'):
            await channel.send('Hello there!')



# bot = discord.Client()
bot.run('tokenhere')
# client = MyClient(intents=intents)
# client.run('bottokenhere')