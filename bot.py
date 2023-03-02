import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} adıyla giriş yapıldı')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()
    if any(word in content.split() for word in
           ['sa', 's.a', 'selamınaleyküm', 'selamın aleyküm', 'selam', 'Selam', 'Sa', 'SA', 'S.a', 'S.A',
            'Selamınaleyküm', 'Selamın aleyküm', 'Selamın Aleyküm', 'selamınaleyküm']):
        await message.channel.send(f'Aleyküm selam , İyi uçuşlar dileriz {message.author.mention} :slight_smile: ')

    await bot.process_commands(message)

@bot.command()
async def timeout(ctx, member: discord.Member, time: int, *, reason=None):
    role = get(ctx.guild.roles, name='Timeout')

    if not role:
        await ctx.send('Timeout adlı bir rol bulunamadı.')
        return

        await member.add_roles(role, reason=reason)
        await asyncio.sleep(time)
        await member.remove_roles(role)
        await ctx.send(f'{member.mention} süreli olarak susturuldu.')

        client = discord.Client()

        # Google API kimlik bilgilerinizi buraya ekleyin
        DEVELOPER_KEY = "AIzaSyBEkEFUDMQObt7lfqS5VZAmHjandSakMqw"
        YOUTUBE_API_SERVICE_NAME = "YouTube Data API"
        YOUTUBE_API_VERSION = "v3"
        CHANNEL_ID = "@turkishaviators2543"
        DISCORD_CHANNEL_ID = "849354281412460567"

        # YouTube kanalını kontrol etmek için fonksiyon oluşturun
        def check_for_new_videos():
            youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

            # Kanalın yayın akışını al
            response = youtube.activities().list(
                part="snippet",
                channelId=CHANNEL_ID,
                maxResults=1
            ).execute()

            # Yeni bir video varsa, Discord kanalına gönder
            if response['items'][0]['snippet']['type'] == 'upload':
                video_id = response['items'][0]['snippet']['resourceId']['videoId']
                video_url = f'https://www.youtube.com/watch?v={video_id}'
                channel = client.get_channel(int(DISCORD_CHANNEL_ID))
                message = f"Yeni bir video geldi! İzlemek için: {video_url}"
                channel.send(message)

        @client.event
        async def on_ready():
            print('Bot is ready!')

            # 10 saniyede bir YouTube kanalını kontrol et
            while True:
                try:
                    check_for_new_videos()
                except HttpError as e:
                    print(f'An HTTP error {e.resp.status} occurred: {e.content}')
                await asyncio.sleep(10)

        client.run('MTA3ODgxMjQ5OTE2MTM5OTM5Ng.G95S4L.-O7mG-nejgfogYMV-i1XK54xtSCI-24noCXaR4')


bot.run('MTA3ODgxMjQ5OTE2MTM5OTM5Ng.G95S4L.-O7mG-nejgfogYMV-i1XK54xtSCI-24noCXaR4')
