import string

import discord
import asyncio

from discord import ClientException
from discord.ext import commands
from discord.utils import get
from gtts import gTTS

translation_table = str.maketrans('', '', string.digits)


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None

    def _play(self, file_name):
        source = discord.FFmpegPCMAudio(source=file_name)
        self.voice_client.play(source)

    def speak(self, speech, lang='en'):
        tts = gTTS(text=speech, lang=lang)
        file_name = f"{speech[:2]}.mp3"

        with open(file_name, 'wb') as f:
            tts.write_to_fp(f)
        self._play(file_name)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        user_name = member.name
        user_name_cleaned = user_name.translate(translation_table)

        if before.channel is None and after.channel:
            if not member.bot:
                try:
                    self.voice_client = await after.channel.connect()
                    self.speak(f"Welcome, {user_name_cleaned}")
                except ClientException:
                    print("Bot is already connected.")
                    self.voice_client.speak(f"Welcome, {user_name_cleaned}")
                except TimeoutError:
                    print(f"Cannot connect to the voice channel {after.channel.id}")


        elif before.channel and after.channel is None:
            bot_voice = get(self.bot.voice_clients, guild=member.guild)
            if bot_voice:
                bot_voice.stop()
                await bot_voice.disconnect(force=True)
