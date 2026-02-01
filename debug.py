import logging

def setup_debug_handlers(bot):
    """Configura handlers de debug globais para todos os comandos."""
    
    @bot.event
    async def on_command(ctx):
        print(f"\n{'='*50}")
        print(f"[DEBUG] Comando: {ctx.command}")
        print(f"[DEBUG] Usuário: {ctx.author} ({ctx.author.id})")
        print(f"[DEBUG] Servidor: {ctx.guild.name} ({ctx.guild.id})")
        print(f"[DEBUG] Canal: {ctx.channel}")
        
        # Verifica permissões do bot
        perms = ctx.guild.me.guild_permissions
        print(f"\n[DEBUG] Permissões do BOT em {ctx.guild.name}:")
        print(f"  👑 Administrador: {perms.administrator}")
        print(f"  🔨 Banir membros: {perms.ban_members}")
        print(f"  🦵 Expulsar membros: {perms.kick_members}")
        print(f"  📝 Gerenciar mensagens: {perms.manage_messages}")
        print(f"  🔇 Moderar membros: {perms.moderate_members}")
        print(f"  👥 Gerenciar cargos: {perms.manage_roles}")
        print(f"  📢 Gerenciar canal: {perms.manage_channels}")
        print(f"{'='*50}\n")
        
        # Log também
        logging.info(f"Comando '{ctx.command}' executado por {ctx.author} em {ctx.guild.name}")

    @bot.event
    async def on_command_error(ctx, error):
        print(f"\n{'!'*50}")
        print(f"[ERRO] Comando: {ctx.command}")
        print(f"[ERRO] Servidor: {ctx.guild.name}")
        print(f"[ERRO] Tipo: {type(error).__name__}")
        print(f"[ERRO] Mensagem: {error}")
        print(f"{'!'*50}\n")
        
        # Log do erro
        logging.error(f"Erro em '{ctx.command}': {error}")
        
        # Enviar mensagem de erro no chat
        try:
            if isinstance(error, commands.MissingPermissions):
                await ctx.send(f"❌ **{ctx.author}**, você não tem permissão: `{error}`")
            elif isinstance(error, commands.BotMissingPermissions):
                await ctx.send(f"⚠️ O bot não tem permissão necessária: `{error}`")
            elif isinstance(error, commands.CheckFailure):
                await ctx.send(f"❌ Verificação de permissão falhou!")
            else:
                await ctx.send(f"❌ Erro: `{error}`")
        except:
            pass  # Ignora erros ao enviar mensagem de erro
