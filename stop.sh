#!/bin/bash

# Script para parar a sessão 'screen' do bot.

SESSION_NAME="bot"

if screen -ls | grep -q "$SESSION_NAME"; then
    echo "🛑 Parando o bot..."
    screen -S $SESSION_NAME -X quit
    echo "✅ Bot parado com sucesso."
else
    echo "⚠️ O bot não parece estar rodando."
fi