# 🤖 Bot Telegram - Sistema de Acessos

## 📁 Arquivos de Controle

### Arquivos Principais de Execução:

- **`start_bot.bat`** - Inicia o bot (versão simples)
- **`start_bot_advanced.bat`** - Inicia o bot (versão avançada com PID)
- **`stop_bot.bat`** - Para o bot (versão simples)
- **`stop_bot_advanced.bat`** - Para o bot (versão avançada)
- **`monitor_bot.bat`** - Monitor em tempo real do bot

## 🚀 Como Usar

### Iniciar o Bot:
1. **Método Simples**: Duplo clique em `start_bot.bat`
2. **Método Avançado**: Duplo clique em `start_bot_advanced.bat`
3. **Com Monitor**: Duplo clique em `monitor_bot.bat` e escolha opção 1

### Parar o Bot:
1. **Método Simples**: Duplo clique em `stop_bot.bat`
2. **Método Avançado**: Duplo clique em `stop_bot_advanced.bat`
3. **Pelo Monitor**: Execute `monitor_bot.bat` e escolha opção 2
4. **Manual**: Pressione `Ctrl+C` na janela do bot

### Monitorar o Bot:
- Execute `monitor_bot.bat` para ver status em tempo real
- Opções disponíveis: Iniciar, Parar, Reiniciar, Ver Logs

## ⚙️ Funcionalidades

### Versão Simples (`start_bot.bat`):
- ✅ Inicia o bot automaticamente
- ✅ Reinstala dependências
- ✅ Reinicia automaticamente se o bot parar
- ✅ Interface colorida

### Versão Avançada (`start_bot_advanced.bat`):
- ✅ Todas as funcionalidades da versão simples
- ✅ Controle por arquivo PID
- ✅ Verificação de instância única
- ✅ Logs com timestamp
- ✅ Melhor controle de processo

### Monitor (`monitor_bot.bat`):
- ✅ Status em tempo real
- ✅ Informações de CPU/Memória
- ✅ Controle completo (Start/Stop/Restart)
- ✅ Visualização de logs
- ✅ Interface interativa

## 🔧 Arquivos de Configuração

- **`bot.config`** - Configurações gerais do bot
- **`requirements.txt`** - Dependências Python
- **`settings/credenciais.json`** - Configurações do bot

## 📝 Logs

- **`bot.log`** - Log principal do bot (se configurado)
- **`bot.pid`** - Arquivo com PID do processo (versão avançada)

## ⚠️ Importante

1. **Nunca feche** a janela do CMD enquanto o bot estiver executando
2. **Use sempre** os scripts de parada para desligar o bot
3. **Mantenha** o arquivo `requirements.txt` atualizado
4. **Configure** as variáveis de ambiente para tokens sensíveis

## 🛠️ Solução de Problemas

### Bot não inicia:
- Verifique se o Python está instalado
- Verifique se o token do bot está correto
- Execute `pip install -r requirements.txt` manualmente

### Bot para sozinho:
- Verifique a conexão com a internet
- Verifique se o token não expirou
- Veja os logs para mais detalhes

### Bot não responde:
- Reinicie usando `monitor_bot.bat`
- Verifique se há erros nos logs
- Teste a conectividade com o Telegram

## 📞 Suporte

Para problemas técnicos, verifique:
1. Logs do bot (`bot.log`)
2. Status no monitor (`monitor_bot.bat`)
3. Configurações em `settings/credenciais.json`

---
*Bot desenvolvido com pyTelegramBotAPI - Versão 3.0.0*