# main.py
import os
import string

from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
from bot import Greetings

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = Intents.default()
translation_table = str.maketrans('', '', string.digits)

bot = commands.Bot(command_prefix='!', intents=intents)

bot.add_cog(Greetings(bot))


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


bot.run(TOKEN)
