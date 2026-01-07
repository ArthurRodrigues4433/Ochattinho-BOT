import discord
from discord.ext import commands
from datetime import timedelta
import settings

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # comando de banir membro
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Bane um membro do servidor."""
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} foi banido do servidor.')


    # comando de expulsar membro
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Expulsa um membro do servidor."""
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} foi expulso do servidor.')


    #comando de silenciar membro
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, duration: int, unit: str):
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
    

    # comando de remover silêncio
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member):
        await member.timeout(None)
        await ctx.send(f'{member} teve o silêncio removido.')


    # comando de limpar mensagens
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)  # +1 para incluir o comando
        await ctx.send(f'{amount} mensagens foram deletadas.', delete_after=5)


    # comando de advertir membro
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        # Aqui você pode armazenar warnings em um banco de dados ou dict
        # Por simplicidade, apenas envia DM
        try:
            await member.send(f'Você foi advertido em {ctx.guild.name}. Razão: {reason}')
            await ctx.send(f'{member} foi advertido.')
        except:
            await ctx.send(f'Não pude enviar DM para {member}.')


async def setup(bot):
    await bot.add_cog(Mod(bot))
