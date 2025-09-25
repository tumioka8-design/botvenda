#!/bin/bash

# Script para atualizar o código do bot a partir do GitHub.

echo "🔄 Puxando as últimas atualizações do GitHub..."
git pull
echo
echo "✅ Código atualizado!"
echo "💡 Lembre-se de parar e iniciar o bot para que as alterações tenham efeito:"
echo "   bash stop.sh"
echo "   bash start.sh"