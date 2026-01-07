import discord
from discord.ext import commands
import yt_dlp
import asyncio

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music_queue = []
        self.current_song = None
        self.music_volume = 0.5  # Volume padrão 50%
        self.queue_lock = asyncio.Lock()

    @commands.command()
    async def join(self, ctx):
        """Faz o bot entrar no canal de voz."""
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect(self_deaf=True)
            await ctx.send(f'Entrei no canal {channel.name}')
        else:
            await ctx.send('Você precisa estar em um canal de voz.')

    @commands.command()
    async def leave(self, ctx):
        """Faz o bot sair do canal de voz."""
        if ctx.voice_client:
            self.music_queue.clear()
            self.current_song = None
            await ctx.voice_client.disconnect()
            await ctx.send('Saí do canal de voz.')
        else:
            await ctx.send('Não estou em um canal de voz.')

    @commands.command()
    async def play(self, ctx, *, query):
        """Adiciona uma música à fila e toca."""
        if len(query) > 200:
            await ctx.send('Query muito longa. Limite: 200 caracteres.')
            return
        if not ctx.voice_client:
            await self.join(ctx)

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 10,
            'extractor_retries': 3,
            'geo_bypass': True,
            'playlistend': 5,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            },
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type: ignore
                if 'youtube.com' in query or 'youtu.be' in query:
                    info = ydl.extract_info(query, download=False)  # type: ignore
                    if 'entries' in info:
                        # É uma playlist
                        for entry in info['entries']:  # type: ignore
                            url = str(entry.get('url'))  # type: ignore
                            title = str(entry.get('title'))  # type: ignore
                            song = {'url': url, 'title': title}
                            self.music_queue.append(song)
                        await ctx.send(f'🎵 Adicionadas {len(info["entries"])} músicas da playlist à fila.')
                    else:
                        # Música única
                        url = str(info.get('url'))  # type: ignore
                        title = str(info.get('title'))  # type: ignore
                        song = {'url': url, 'title': title}
                        self.music_queue.append(song)
                        print(f"Adicionada música à fila: {title}")
                        await ctx.send(f'🎵 Adicionado à fila: {title}')
                else:
                    # Busca por nome
                    search_info = ydl.extract_info(f'ytsearch:{query}', download=False)  # type: ignore
                    info = search_info['entries'][0]  # type: ignore
                    url = str(info.get('url'))  # type: ignore
                    title = str(info.get('title'))  # type: ignore
                    song = {'url': url, 'title': title}
                    self.music_queue.append(song)
                    print(f"Adicionada música à fila: {title}")
                    print(f"Adicionada música à fila: {title}")
                    await ctx.send(f'🎵 Adicionado à fila: {title}')

                if not ctx.voice_client.is_playing():
                    await self.play_next(ctx)
        except Exception as e:
            await ctx.send(f'Erro ao adicionar música: {str(e)}')

    async def play_next(self, ctx):
        if self.music_queue:
            song = self.music_queue.pop(0)
            self.current_song = song
            source = discord.FFmpegPCMAudio(song['url'], executable='/usr/local/bin/ffmpeg')
            source = discord.PCMVolumeTransformer(source, volume=self.music_volume)
            ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))
            await ctx.send(f'🎵 Tocando: {song["title"]}')
        else:
            self.current_song = None
            # Agendar saída automática após 30 segundos se não houver música
            await asyncio.sleep(30)
            if not ctx.voice_client.is_playing() and not self.music_queue:
                await ctx.voice_client.disconnect()
                await ctx.send('Saí do canal de voz pois não há mais músicas.')

    @commands.command()
    async def skip(self, ctx):
        """Pula a música atual."""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send('Música pulada.')
        else:
            await ctx.send('Nenhuma música está tocando.')

    @commands.command()
    async def pause(self, ctx):
        """Pausa a música."""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send('Música pausada.')
        else:
            await ctx.send('Nenhuma música está tocando.')

    @commands.command()
    async def resume(self, ctx):
        """Retoma a música."""
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send('Música retomada.')
        else:
            await ctx.send('A música não está pausada.')

    @commands.command()
    async def queue(self, ctx):
        """Mostra a fila de músicas."""
        if self.music_queue:
            embed = discord.Embed(title='🎵 Fila de Músicas', color=discord.Color.blue())
            for i, song in enumerate(self.music_queue, 1):
                embed.add_field(name=f'{i}. {song["title"]}', value='\u200b', inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send('A fila está vazia.')

    @commands.command()
    async def volume(self, ctx, vol: int):
        """Ajusta o volume (0-100)."""
        if 0 <= vol <= 100:
            self.music_volume = vol / 100
            if ctx.voice_client and ctx.voice_client.source:
                ctx.voice_client.source.volume = self.music_volume
            await ctx.send(f'Volume ajustado para {vol}%.')
        else:
            await ctx.send('Volume deve ser entre 0 e 100.')

    @commands.command()
    async def stop(self, ctx):
        """Para a música e limpa a fila."""
        if ctx.voice_client:
            self.music_queue.clear()
            self.current_song = None
            ctx.voice_client.stop()
            await ctx.send('Música parada e fila limpa.')
        else:
            await ctx.send('Não estou em um canal de voz.')

async def setup(bot):
    await bot.add_cog(Music(bot))
