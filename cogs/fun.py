import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def dice(self, ctx):
        result = random.randint(1, 6)
        await ctx.send(f'🎲 Você rolou um {result}!')

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def coinflip(self, ctx):
        result = random.choice(['Cara', 'Coroa'])
        await ctx.send(f'🪙 A moeda caiu em: {result}!')

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def meme(self, ctx):
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
    await bot.add_cog(Fun(bot))