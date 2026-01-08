"""
Cog para comandos de diversão.
Inclui comandos simples como ping, rolagem de dado, cara ou coroa e memes.
"""

import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    """
    Classe para comandos divertidos.
    Comandos com cooldown para evitar spam.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        """Responde com Pong! para testar a latência."""
        await ctx.send('Pong!')

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def dice(self, ctx):
        """Rola um dado de 6 faces e mostra o resultado."""
        result = random.randint(1, 6)
        await ctx.send(f'🎲 Você rolou um {result}!')

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def coinflip(self, ctx):
        """Joga uma moeda e mostra se caiu cara ou coroa."""
        result = random.choice(['Cara', 'Coroa'])
        await ctx.send(f'🪙 A moeda caiu em: {result}!')

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def meme(self, ctx):
        """Envia um meme aleatório da lista pré-definida."""
        memes = [
            'Por que o computador foi ao médico? Porque tinha um vírus!',
            'O que o zero disse para o oito? Belo cinto!',
            'Por que a galinha atravessou a estrada? Para chegar do outro lado!',
            'O que é um fantasma? Um espírito sem corpo!',
            'Por que o livro de matemática estava triste? Porque tinha muitos problemas!'
        ]
        meme = random.choice(memes)
        await ctx.send(f'😂 {meme}')


async def setup(bot):
    """Função de configuração para adicionar a cog Fun ao bot."""
    await bot.add_cog(Fun(bot))