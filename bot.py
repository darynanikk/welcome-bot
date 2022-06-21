import string
import discord

from discord.ext import commands
from discord.utils import get
from gtts import gTTS

translation_table = str.maketrans('', '', string.digits)


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None
        self._last_member = None

    def _play(self, file_name):
        source = discord.FFmpegPCMAudio(source=file_name, options="-loglevel panic")
        self.voice_client.play(source)

    def speak(self, speech, lang='en'):
        tts = gTTS(text=speech, lang=lang)
        file_name = f"{speech[:2]}.mp3"

        with open(file_name, 'wb') as f:
            tts.write_to_fp(f)
        self._play(file_name)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        user_name = member.name if self._last_member is None else self._last_member.name
        user_name_cleaned = user_name.translate(translation_table)
        bot_voice = get(self.bot.voice_clients, guild=member.guild)

        if before.channel is None and after.channel:
            if not bot_voice:
                self.voice_client = await after.channel.connect(reconnect=True)
                self.speak(f"Welcome, {user_name_cleaned}")
            else:
                if self.voice_client:
                    if bot_voice.channel.id != after.channel.id:
                        await bot_voice.disconnect(force=True)
                        await bot_voice.move_to(after.channel)
                    else:
                        self.speak(f"Welcome, {user_name_cleaned}")
            if not member.bot:
                self._last_member = member

        elif before.channel and after.channel is None:
            # only bot left in the guild
            if bot_voice and len(bot_voice.guild.members) == 1:
                self.voice_client = None
                self._last_member = None
                await bot_voice.disconnect(force=True)
        else:
            if self.voice_client:
                if self.voice_client.is_playing():
                    self.voice_client.stop()
                return
