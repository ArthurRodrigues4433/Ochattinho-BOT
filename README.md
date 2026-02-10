# Ochattinho BOT

![Bot Discord](image.png)

Um bot Discord multifuncional escrito em Python usando discord.py, com comandos de diversão, moderação, administração, música e utilitários.

## Deploy

O bot está hospedado no **fly.io** e faz deploy automático via GitHub Actions.

### Status
- **Produção**: https://ochattinho-bot.fly.dev
- **Deploy**: Automático ao fazer push na branch `master`

### Deploy Manual

```bash
# Instalar flyctl
iwr https://fly.io/install.ps1 -useb | iex

# Login
flyctl auth login

# Deploy
flyctl deploy --app ochattinho-bot
```

## Funcionalidades

- **Diversão**: Comandos como ping, dado, moeda, memes.
- **Moderação**: Ban, kick, mute, clear, warn.
- **Administração**: Configuração de prefixo, logs, roles, reload de cogs, shutdown.
- **Música**: Reprodução de músicas do YouTube com fila.
- **Utilitários**: Info de servidor, usuário, canal, bot, uptime, invite.

## Instalação Local

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

- O bot usa prefixo dinâmico por servidor (padrão: `oc!`).
- Configurações são salvas em `settings.json`.
- Logs são gravados no console e em arquivos para ações admin.

## Comandos

### Diversão
- `oc!ping` - Responde com Pong!
- `oc!dice` - Rola um dado (1-6)
- `oc!coinflip` - Cara ou coroa
- `oc!meme` - Piada aleatória

### Utilitários
- `oc!serverinfo` - Info do servidor
- `oc!userinfo [@user]` - Info do usuário
- `oc!avatar [@user]` - Avatar do usuário
- `oc!roleinfo @role` - Info da role
- `oc!channelinfo` - Info do canal
- `oc!botinfo` - Info do bot
- `oc!uptime` - Tempo online
- `oc!invite` - Link de convite
- `oc!ajuda` - Lista de comandos

### Moderação (Requer permissões)
- `oc!ban @user [reason]` - Bane usuário
- `oc!kick @user [reason]` - Expulsa usuário
- `oc!mute @user duration unit` - Silencia usuário
- `oc!unmute @user` - Remove silêncio
- `oc!clear amount` - Limpa mensagens
- `oc!warn @user [reason]` - Adverte usuário

### Administração (Apenas admins)
- `oc!setprefix <prefix>` - Altera prefixo
- `oc!setlog #channel` - Define canal de logs
- `oc!setmodrole @role` - Define role de mod
- `oc!reload <cog>` - Recarrega cog
- `oc!shutdown` - Desliga bot

### Música
- `oc!join` - Entra no canal de voz
- `oc!leave` - Sai do canal
- `oc!play <query>` - Toca música
- `oc!skip` - Pula música
- `oc!pause` - Pausa
- `oc!resume` - Retoma
- `oc!queue` - Mostra fila
- `oc!volume <0-100>` - Ajusta volume
- `oc!stop` - Para e limpa fila

## Segurança

- Rate limiting em comandos de diversão.
- Validação de entradas (ex: limite de 200 chars em queries de música).
- Logs de ações administrativas.
- Tratamento seguro de erros (não expõe stack traces).
- Token armazenado em variável de ambiente ou secrets.

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
- `.env` - Variáveis de ambiente (não commitado)
- `settings.json` - Configurações salvas
- `fly.toml` - Configuração do fly.io
- `Dockerfile` - Container Docker

## Contribuição

Sinta-se à vontade para contribuir com issues ou pull requests.

## Licença

Este projeto é open-source. Fique a vontade para contribuir.
