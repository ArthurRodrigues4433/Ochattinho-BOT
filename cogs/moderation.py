"""
Cog para comandos de moderação.
Inclui comandos para banir, expulsar, silenciar, limpar mensagens e advertir membros.
"""

import discord
from discord.ext import commands
from datetime import timedelta
import settings

class Mod(commands.Cog):
    """
    Classe para comandos de moderação.
    Requer permissões específicas para cada comando.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Bane um membro do servidor."""
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} foi banido do servidor.')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Expulsa um membro do servidor."""
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} foi expulso do servidor.')

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, duration: int, unit: str):
        """Silencia um membro por um período especificado (m: minutos, h: horas, d: dias)."""
        # Converte a unidade para timedelta
        if unit.lower() == 'm':
            delta = timedelta(minutes=duration)
        elif unit.lower() == 'h':
            delta = timedelta(hours=duration)
        elif unit.lower() == 'd':
            delta = timedelta(days=duration)
        else:
            await ctx.send('Unidade inválida. Use m (minutos), h (horas) ou d (dias).')
            return
        await member.timeout(delta)
        await ctx.send(f'{member} foi silenciado por {duration}{unit}.')

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member):
        """Remove o silêncio de um membro."""
        await member.timeout(None)
        await ctx.send(f'{member} teve o silêncio removido.')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        """Limpa um número especificado de mensagens do canal."""
        await ctx.channel.purge(limit=amount + 1)  # +1 para incluir o comando
        await ctx.send(f'{amount} mensagens foram deletadas.', delete_after=5)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        """Adverte um membro enviando uma DM. Para armazenamento persistente, use um banco de dados."""
        # Aqui você pode armazenar warnings em um banco de dados ou dict
        # Por simplicidade, apenas envia DM
        try:
            await member.send(f'Você foi advertido em {ctx.guild.name}. Razão: {reason}')
            await ctx.send(f'{member} foi advertido.')
        except:
            await ctx.send(f'Não pude enviar DM para {member}.')


async def setup(bot):
    """Função de configuração para adicionar a cog Mod ao bot."""
    await bot.add_cog(Mod(bot))
