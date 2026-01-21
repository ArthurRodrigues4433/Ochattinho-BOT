import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os

# =========================
# PATH DO COOKIE (ABSOLUTO)
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COOKIE_PATH = os.path.join(BASE_DIR, 'cookies.txt')


def get_best_audio(info: dict) -> str:
    """
    Retorna a melhor URL de áudio disponível para streaming.
    """
    formats = info.get("formats", [])
    for f in formats:
        if f.get("acodec") != "none" and f.get("url"):
            return f["url"]
    return info.get("url") #type: ignore


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music_queue = []
        self.current_song = None
        self.music_volume = 0.5
        self.queue_lock = asyncio.Lock()

    # =========================
    # VOICE
    # =========================
    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if not ctx.voice_client:
                await channel.connect(self_deaf=True)
            await ctx.send(f'🎧 Entrei no canal **{channel.name}**')
        else:
            await ctx.send('❌ Você precisa estar em um canal de voz.')

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            self.music_queue.clear()
            self.current_song = None
            await ctx.voice_client.disconnect()
            await ctx.send('👋 Saí do canal de voz.')
        else:
            await ctx.send('❌ Não estou em um canal de voz.')

    # =========================
    # PLAY
    # =========================
    @commands.command()
    async def play(self, ctx, *, query: str):
        if len(query) > 200:
            await ctx.send('❌ Query muito longa (máx. 200 caracteres).')
            return

        if not ctx.voice_client:
            await self.join(ctx)

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'cookiefile': COOKIE_PATH,
            'noplaylist': True,
            'skip_download': True,
            'force_ipv4': True,
            'extract_flat': False,
        }

        try:
            async with self.queue_lock:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl: #type: ignore
                    if 'youtube.com' in query or 'youtu.be' in query:
                        info = ydl.extract_info(query, download=False)
                    else:
                        search = ydl.extract_info(f'ytsearch:{query}', download=False)
                        info = search['entries'][0] #type: ignore

                    if 'entries' in info:
                        info = info['entries'][0]

                    audio_url = get_best_audio(info) #type: ignore
                    title = info.get('title', 'Sem título')

                    song = {
                        'url': audio_url,
                        'title': title
                    }

                    self.music_queue.append(song)
                    await ctx.send(f'🎵 Adicionado à fila: **{title}**')

                if not ctx.voice_client.is_playing():
                    await self.play_next(ctx)

        except Exception as e:
            await ctx.send(f'❌ Erro ao tocar música: `{e}`')

    # =========================
    # PLAYER
    # =========================
    async def play_next(self, ctx):
        if not self.music_queue:
            self.current_song = None
            await self.disconnect_if_idle(ctx)
            return

        song = self.music_queue.pop(0)
        self.current_song = song

        source = discord.FFmpegPCMAudio(
            song['url'],
            before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -loglevel panic',
            options='-vn'
        )

        source = discord.PCMVolumeTransformer(source, volume=self.music_volume)

        ctx.voice_client.play(
            source,
            after=lambda e: asyncio.run_coroutine_threadsafe(
                self.song_ended(ctx),
                self.bot.loop
            )
        )

        await ctx.send(f'▶️ Tocando agora: **{song["title"]}**')

    async def song_ended(self, ctx):
        await self.play_next(ctx)

    async def disconnect_if_idle(self, ctx):
        if ctx.voice_client and not ctx.voice_client.is_playing() and not self.music_queue:
            await ctx.voice_client.disconnect()
            await ctx.send('⏹️ Saí do canal (fila vazia).')

    # =========================
    # CONTROLES
    # =========================
    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send('⏭️ Música pulada.')
        else:
            await ctx.send('❌ Nenhuma música tocando.')

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send('⏸️ Música pausada.')
        else:
            await ctx.send('❌ Nenhuma música tocando.')

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send('▶️ Música retomada.')
        else:
            await ctx.send('❌ A música não está pausada.')

    @commands.command()
    async def queue(self, ctx):
        if not self.music_queue:
            await ctx.send('📭 A fila está vazia.')
            return

        embed = discord.Embed(title='🎶 Fila de Músicas', color=discord.Color.blue())
        for i, song in enumerate(self.music_queue, start=1):
            embed.add_field(name=f'{i}. {song["title"]}', value='\u200b', inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def volume(self, ctx, vol: int):
        if 0 <= vol <= 100:
            self.music_volume = vol / 100
            if ctx.voice_client and ctx.voice_client.source:
                ctx.voice_client.source.volume = self.music_volume
            await ctx.send(f'🔊 Volume ajustado para {vol}%.')
        else:
            await ctx.send('❌ Volume deve estar entre 0 e 100.')

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client:
            self.music_queue.clear()
            self.current_song = None
            ctx.voice_client.stop()
            await ctx.send('⏹️ Música parada e fila limpa.')
        else:
            await ctx.send('❌ Não estou em um canal de voz.')


async def setup(bot):
    await bot.add_cog(Music(bot))
