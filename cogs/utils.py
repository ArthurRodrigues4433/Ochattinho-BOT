import discord
from discord.ext import commands
from typing import Optional
import datetime


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.datetime.utcnow()

    @commands.command()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(
            title=f"📊 {guild.name}", description=guild.description or "Sem descrição"
        )
        embed.add_field(name="👥 Membros", value=guild.member_count)
        embed.add_field(
            name="📅 Criado em", value=guild.created_at.strftime("%d/%m/%Y")
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        await ctx.send(embed=embed)

    @commands.command()
    async def userinfo(self, ctx, member: Optional[discord.Member] = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"👤 {member.name}", color=member.color)
        embed.add_field(name="🆔 ID", value=member.id)
        embed.add_field(
            name="📅 Entrou em",
            value=member.joined_at.strftime("%d/%m/%Y") if member.joined_at else "N/A",
        )
        embed.add_field(
            name="📅 Conta criada", value=member.created_at.strftime("%d/%m/%Y")
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        await ctx.send(embed=embed)

    @commands.command()
    async def avatar(self, ctx, member: Optional[discord.Member] = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"Avatar de {member.name}")
        embed.set_image(
            url=member.avatar.url if member.avatar else member.default_avatar.url
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def roleinfo(self, ctx, role: discord.Role):
        embed = discord.Embed(title=f"Role: {role.name}", color=role.color)
        embed.add_field(name="ID", value=role.id)
        embed.add_field(name="Cor", value=str(role.color))
        embed.add_field(name="Membros", value=len(role.members))
        embed.add_field(name="Criado em", value=role.created_at.strftime("%d/%m/%Y"))
        await ctx.send(embed=embed)

    @commands.command()
    async def channelinfo(self, ctx):
        channel = ctx.channel
        embed = discord.Embed(title=f"Canal: {channel.name}")
        embed.add_field(name="ID", value=channel.id)
        embed.add_field(name="Tipo", value=str(channel.type))
        if isinstance(channel, discord.TextChannel):
            embed.add_field(name="NSFW", value="Sim" if channel.nsfw else "Não")
            embed.add_field(
                name="Criado em", value=channel.created_at.strftime("%d/%m/%Y")
            )
        await ctx.send(embed=embed)

    @commands.command()
    async def botinfo(self, ctx):
        embed = discord.Embed(
            title="Bot Info", description=f"Bot: {self.bot.user.name}"
        )
        embed.add_field(name="ID", value=self.bot.user.id)
        embed.add_field(
            name="Criado em", value=self.bot.user.created_at.strftime("%d/%m/%Y")
        )
        embed.add_field(name="Servidores", value=len(self.bot.guilds))
        embed.add_field(name="Usuários", value=len(self.bot.users))
        embed.set_thumbnail(
            url=self.bot.user.avatar.url if self.bot.user.avatar else None
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def uptime(self, ctx):
        now = datetime.datetime.utcnow()
        delta = now - self.start_time
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        embed = discord.Embed(
            title="Uptime", description=f"{days}d {hours}h {minutes}m {seconds}s"
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        invite_link = f"https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=8"
        embed = discord.Embed(
            title="Invite Link",
            description=f"[Clique aqui para convidar o bot]({invite_link})",
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def ajuda(self, ctx):
        embed = discord.Embed(
            title="🤖 Central de Comandos — Ochattinho BOT",
            description=(
                "Aqui estão todos os comandos disponíveis.\n"
                "Use o prefixo **!** antes de cada comando."
            ),
            color=discord.Color.blurple(),
        )

        # 🎉 Diversão
        embed.add_field(
            name="🎉 Diversão",
            value=(
                "**`!ping`** — Mostra o ping do bot\n"
                "**`!dice`** — Rola um dado aleatório 🎲\n"
                "**`!coinflip`** — Cara ou coroa 🪙\n"
                "**`!meme`** — Envia um meme aleatório 😂"
            ),
            inline=False,
        )

        # 🎵 Música
        embed.add_field(
            name="🎵 Música",
            value=(
                "**`!join`** — Entra no canal de voz\n"
                "**`!leave`** — Sai do canal de voz\n"
                "**`!play <nome ou link>`** — Toca ou adiciona à fila\n"
                "**`!skip`** — Pula a música atual ⏭️\n"
                "**`!pause`** — Pausa a música ⏸️\n"
                "**`!resume`** — Retoma a música ▶️\n"
                "**`!queue`** — Mostra a fila de músicas 🎶\n"
                "**`!volume <0-100>`** — Ajusta o volume 🔊\n"
                "**`!stop`** — Para tudo e limpa a fila ⏹️"
            ),
            inline=False,
        )

        # 🛠️ Utilitários
        embed.add_field(
            name="🛠️ Utilitários",
            value=(
                "**`!serverinfo`** — Informações do servidor\n"
                "**`!userinfo`** — Informações de um usuário\n"
                "**`!avatar`** — Mostra o avatar\n"
                "**`!roleinfo`** — Informações de um cargo\n"
                "**`!channelinfo`** — Informações do canal\n"
                "**`!botinfo`** — Informações do bot\n"
                "**`!uptime`** — Tempo online ⏱️\n"
                "**`!invite`** — Link para adicionar o bot\n"
                "**`!ajuda`** — Mostra esta lista"
            ),
            inline=False,
        )

        # 🛡️ Moderação
        embed.add_field(
            name="🛡️ Moderação",
            value=(
                "⚠️ *Apenas moderadores*\n"
                "**`!ban`** — Bane um usuário\n"
                "**`!kick`** — Expulsa um usuário\n"
                "**`!mute`** — Silencia um usuário\n"
                "**`!unmute`** — Remove o silêncio\n"
                "**`!clear`** — Limpa mensagens\n"
                "**`!warn`** — Aplica um aviso"
            ),
            inline=False,
        )

        # ⚙️ Administração
        embed.add_field(
            name="⚙️ Administração",
            value=(
                "🚫 *Apenas administradores*\n"
                "**`!setprefix`** — Altera o prefixo\n"
                "**`!setlog`** — Define canal de logs\n"
                "**`!setmodrole`** — Define cargo de moderador\n"
                "**`!reload`** — Recarrega módulos\n"
                "**`!shutdown`** — Desliga o bot"
            ),
            inline=False,
        )

        embed.set_footer(text="💡 Dica: use !ajuda para ver todos os comandos")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Utils(bot))
