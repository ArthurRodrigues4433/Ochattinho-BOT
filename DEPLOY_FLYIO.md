# Deploy no Fly.io

## Pré-requisitos

1. Conta no [Fly.io](https://fly.io)
2. Fly CLI instalado

## Instalação do Fly CLI

### Windows (PowerShell):
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

### Ou via npm:
```bash
npm install -g flyctl
```

## Configuração Inicial

### 1. Fazer login
```bash
flyctl auth login
```

### 2. Definir variáveis de ambiente (seguras)
```bash
flyctl secrets set TOKEN="seu_token_do_bot_discord_aqui"
```

### 3. Criar o app no fly.io (se ainda não existir)
```bash
flyctl apps create ochattinho-bot
```

## Deploy

### Deploy padrão
```bash
flyctl deploy
```

### Deploy com configuração específica
```bash
flyctl deploy --config fly.toml
```

## Comandos Úteis

### Ver status do app
```bash
flyctl status
```

### Ver logs
```bash
flyctl logs
```

### Abrir console remoto
```bash
flyctl ssh console
```

### Escalar recursos
```bash
flyctl vm resize
```

### Ver métricas
```bash
flyctl metrics
```

### Restartar o bot
```bash
flyctl restart
```

### Destruir o app (cuidado!)
```bash
flyctl apps destroy ochattinho-bot
```

## Configurações do fly.toml

O arquivo [`fly.toml`](fly.toml) já está configurado com:
- **Região**: São Paulo (gru)
- **VM**: shared-cpu-1x com 1GB RAM
- **Auto-stop**: O app para quando não há uso

## Variáveis de Ambiente Necessárias

O bot precisa de:
- `TOKEN` - Token do bot Discord

## Solução de Problemas

### Log de erros
```bash
flyctl logs -t
```

### Verificar status das máquinas
```bash
flyctl machine list
```

### Reconectar após falha
```bash
flyctl deploy --force
```

## Custo Estimado

O app está configurado com recursos mínimos:
- VM: shared-cpu-1x (~$1.94/mês por 1GB RAM)
- O bot para automaticamente quando inativo
