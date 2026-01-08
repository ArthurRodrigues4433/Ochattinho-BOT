"""
Arquivo principal do bot Discord.
Inicializa o bot, configura logging e carrega as extensões (cogs).
"""

import os
import discord
from discord.ext import commands
import bot_config
import settings
import logging

# Configuração do logging para registrar eventos do bot
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para obter o prefixo do comando baseado no servidor (guild)
def get_prefix(bot, message):
    return settings.PREFIXES.get(message.guild.id if message.guild else None, '!')

# Inicialização do bot com prefixo dinâmico e todas as intents habilitadas
bot = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all())
bot.remove_command('help')  # Remove o comando de ajuda padrão para implementar um customizado

@bot.event
async def on_ready():
    """
    Evento chamado quando o bot está conectado e pronto para uso.
    Carrega automaticamente todas as extensões (cogs) da pasta ./cogs.
    """
    print(f'Bot inicializado: {bot.user}')
    # Carregar cogs
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            print(f"Tentando carregar: {filename}")
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"Carregado com sucesso: {filename}")
            except Exception as e:
                print(f"Erro ao carregar {filename}: {e}")

# Verifica se o token do bot está configurado antes de executar
assert bot_config.TOKEN is not None, "TOKEN não configurado"
bot.run(bot_config.TOKEN)
