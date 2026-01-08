import os
import discord
from discord.ext import commands
import bot_config
import settings
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_prefix(bot, message):
    return settings.PREFIXES.get(message.guild.id if message.guild else None, '!')

bot = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all())
bot.remove_command('help')

@bot.event
async def on_ready():
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

assert bot_config.TOKEN is not None, "TOKEN não configurado"
bot.run(bot_config.TOKEN)
