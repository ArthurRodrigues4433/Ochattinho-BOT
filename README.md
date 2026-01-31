# Ochattinho BOT

![Bot Discord](image.png)

Um bot Discord multifuncional escrito em Python usando discord.py, com comandos de diversão, moderação, administração, música e utilitários.


## Funcionalidades

- **Diversão**: Comandos como ping, dado, moeda, memes.
- **Moderação**: Ban, kick, mute, clear, warn.
- **Administração**: Configuração de prefixo, logs, roles, reload de cogs, shutdown.
- **Música**: Reprodução de músicas do YouTube com fila.
- **Utilitários**: Info de servidor, usuário, canal, bot, uptime, invite.

## Instalação

1. Clone o repositório:
   ```bash
   git clone <url-do-repo>
   cd ochattinho-bot
   ```

2. Instale as dependências:
   ```bash
   pip install discord.py yt-dlp python-dotenv
   ```

3. Configure o arquivo `.env`:
   ```
   TOKEN=seu_token_aqui
   ```

4. Execute o bot:
   ```bash
   python main.py
   ```

## Configuração

- O bot usa prefixo dinâmico por servidor (padrão: `!`).
- Configurações são salvas em `settings.json`.
- Logs são gravados no console e em arquivos para ações admin.

## Comandos

### Diversão
- `!ping` - Responde com Pong!
- `!dice` - Rola um dado (1-6)
- `!coinflip` - Cara ou coroa
- `!meme` - Piada aleatória

### Utilitários
- `!serverinfo` - Info do servidor
- `!userinfo [@user]` - Info do usuário
- `!avatar [@user]` - Avatar do usuário
- `!roleinfo @role` - Info da role
- `!channelinfo` - Info do canal
- `!botinfo` - Info do bot
- `!uptime` - Tempo online
- `!invite` - Link de convite
- `!ajuda` - Lista de comandos

### Moderação (Requer permissões)
- `!ban @user [reason]` - Bane usuário
- `!kick @user [reason]` - Expulsa usuário
- `!mute @user duration unit` - Silencia usuário
- `!unmute @user` - Remove silêncio
- `!clear amount` - Limpa mensagens
- `!warn @user [reason]` - Adverte usuário

### Administração (Apenas admins)
- `!setprefix <prefix>` - Altera prefixo
- `!setlog #channel` - Define canal de logs
- `!setmodrole @role` - Define role de mod
- `!reload <cog>` - Recarrega cog
- `!shutdown` - Desliga bot

### Música
- `!join` - Entra no canal de voz
- `!leave` - Sai do canal
- `!play <query>` - Toca música
- `!skip` - Pula música
- `!pause` - Pausa
- `!resume` - Retoma
- `!queue` - Mostra fila
- `!volume <0-100>` - Ajusta volume
- `!stop` - Para e limpa fila

## Segurança

- Rate limiting em comandos de diversão.
- Validação de entradas (ex: limite de 200 chars em queries de música).
- Logs de ações administrativas.
- Tratamento seguro de erros (não expõe stack traces).
- Token armazenado em `.env`.

## Estrutura do Projeto

- `main.py` - Arquivo principal
- `config.py` - Configurações
- `settings.py` - Gerenciamento de configurações dinâmicas
- `cogs/` - Módulos do bot
  - `admin.py` - Comandos admin
  - `fun.py` - Comandos de diversão
  - `moderation.py` - Comandos de moderação
  - `music.py` - Comandos de música
  - `utils.py` - Comandos utilitários
- `test_settings.py` - Testes básicos
- `.env` - Variáveis de ambiente
- `settings.json` - Configurações salvas

## Contribuição

Sinta-se à vontade para contribuir com issues ou pull requests.

## Licença

Este projeto é open-source. Use por sua conta e risco.