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
import debug

# Configuração do logging para registrar eventos do bot
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Função para obter o prefixo do comando baseado no servidor (guild)
def get_prefix(bot, message):
    return settings.PREFIXES.get(message.guild.id if message.guild else None, "oc!")


def encontrar_canal_disponivel(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            return channel
    return None


# Inicialização do bot com prefixo dinâmico e todas as intents habilitadas
bot = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all())
bot.remove_command(
    "help"
)  # Remove o comando de ajuda padrão para implementar um customizado


@bot.event
async def on_guild_join(guild):
    """Evento chamado quando o bot entra em um servidor."""
    canal = encontrar_canal_disponivel(guild)

    required_permissions = discord.Permissions(
        send_messages=True,
        embed_links=True,
        read_messages=True,
        read_message_history=True,
        add_reactions=True,
    )

    bot_permissions = guild.me.guild_permissions

    missing_perms = []
    for perm_name, value in required_permissions:
        if not getattr(bot_permissions, perm_name):
            missing_perms.append(perm_name)

    if missing_perms:
        print(f"[AVISO] Bot entrou em {guild.name} sem permissões: {missing_perms}")

        # Verifica hierarquia ANTES de sair
        bot_role = guild.me.top_role
        highest_role = max(guild.roles, key=lambda r: r.position)
        if guild.me != guild.owner and bot_role.position < highest_role.position:
            print(f"[AVISO] Cargo do bot não está no topo em {guild.name}")

        # Envia mensagem no primeiro canal disponível
        if canal:
            try:
                await canal.send(
                    f"⚠️ Olá! Eu sou o **Ochattinho BOT**!\n"
                    f"Percebi que não tenho as permissões necessárias para funcionar corretamente.\n"
                    f"Permissões faltando: {', '.join(missing_perms)}\n"
                    f"Por favor, ajuste minhas permissões e me adicione novamente!"
                )
            except:
                print(f"Não consegui enviar mensagem de aviso em {guild.name}")

        await guild.leave()
        print(f"Sai de {guild.name} por falta de permissões")

    else:
        print(f"[INFO] Bot entrou com sucesso em {guild.name}!")

        if canal:
            try:
                await canal.send(
                    f"🎉 Olá! Eu sou o **Ochattinho BOT**!\n"
                    f"Estou pronto para ajudar em **{guild.name}**.\n"
                    f"Use `oc!ajuda` para ver meus comandos!"
                )
            except:
                pass

        # Verifica hierarquia se entrou com permissões OK
        bot_role = guild.me.top_role
        highest_role = max(guild.roles, key=lambda r: r.position)
        if guild.me != guild.owner and bot_role.position < highest_role.position:
            print(f"[AVISO] Cargo do bot não está no topo em {guild.name}")


@bot.event
async def on_ready():
    """
    Evento chamado quando o bot está conectado e pronto para uso.
    Carrega automaticamente todas as extensões (cogs) da pasta ./cogs.
    """
    print(f"Bot inicializado: {bot.user}")
    # Carregar cogs
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            print(f"Tentando carregar: {filename}")
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"Carregado com sucesso: {filename}")
            except Exception as e:
                print(f"Erro ao carregar {filename}: {e}")


# Verifica se o token do bot está configurado antes de executar
assert bot_config.TOKEN is not None, "TOKEN não configurado"
debug.setup_debug_handlers(bot)
bot.run(bot_config.TOKEN)
