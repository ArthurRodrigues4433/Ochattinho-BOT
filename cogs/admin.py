"""
Cog para comandos de administração do bot.
Permite configurar prefixo, canal de log, role de moderação, recarregar cogs e desligar o bot.
"""

import discord
from discord.ext import commands
import settings
import logging


class Admin(commands.Cog):
    """
    Classe para comandos administrativos.
    Requer permissões de administrador para uso.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, prefix: str):
        """Define o prefixo dos comandos para o servidor atual."""
        settings.PREFIXES[ctx.guild.id] = prefix
        settings.save_settings()
        logging.info(f"Prefix changed to {prefix} by {ctx.author} in {ctx.guild}")
        await ctx.send(f"Prefixo alterado para `{prefix}`")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlog(self, ctx, channel: discord.TextChannel):
        """Define o canal de log para o servidor atual."""
        settings.LOG_CHANNELS[ctx.guild.id] = channel.id
        settings.save_settings()
        logging.info(f"Log channel set to {channel} by {ctx.author} in {ctx.guild}")
        await ctx.send(f"Canal de log definido para {channel.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setmodrole(self, ctx, role: discord.Role):
        """Define a role de moderação para o servidor atual."""
        settings.MOD_ROLES[ctx.guild.id] = role.id
        settings.save_settings()
        logging.info(f"Mod role set to {role} by {ctx.author} in {ctx.guild}")
        await ctx.send(f"Role de moderação definida para {role.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx, cog: str):
        """Recarrega uma cog específica do bot."""
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
            logging.info(f"Cog {cog} reloaded by {ctx.author} in {ctx.guild}")
            await ctx.send(f"Cog `{cog}` recarregada com sucesso.")
        except Exception as e:
            logging.error(f"Error reloading cog {cog}: {e}")
            await ctx.send("Erro interno ao recarregar cog.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def shutdown(self, ctx):
        """Desliga o bot."""
        logging.info(f"Bot shutdown initiated by {ctx.author} in {ctx.guild}")
        await ctx.send("Desligando o bot...")
        await self.bot.close()


async def setup(bot):
    """Função de configuração para adicionar a cog Admin ao bot."""
    await bot.add_cog(Admin(bot))
