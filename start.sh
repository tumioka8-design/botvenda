#!/bin/bash

# Script para iniciar o bot em uma sessão 'screen'.

SESSION_NAME="bot"

# Verifica se a sessão já existe
if screen -ls | grep -q "$SESSION_NAME"; then
    echo "✅ O bot já está rodando em segundo plano."
    echo "💡 Para ver os logs, use o comando: screen -r $SESSION_NAME"
else
    echo "🚀 Iniciando o bot em segundo plano..."
    # Inicia o bot dentro de uma sessão screen desanexada
    screen -dmS $SESSION_NAME python bot.py
    echo "✅ Bot iniciado com sucesso!"
    echo "💡 Para ver os logs, use o comando: screen -r $SESSION_NAME"
fi