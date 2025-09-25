@echo off
chcp 65001 >nul
title GitHub Uploader - Perky Logins Bot
color 0a
setlocal enabledelayedexpansion

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                   GITHUB UPLOADER                            ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM --- 1. VERIFICAR SE O GIT ESTÁ INSTALADO ---
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERRO: Git não foi encontrado no seu sistema.
    echo.
    echo 💡 Por favor, instale o Git a partir de: git-scm.com/download/win
    echo    Após a instalação, feche e abra este script novamente.
    echo.
    pause
    exit /b
)
echo ✅ Git encontrado!
echo.

REM --- 2. MUDAR PARA O DIRETÓRIO DO SCRIPT ---
cd /d "%~dp0"

REM --- 3. VERIFICAR SE JÁ É UM REPOSITÓRIO GIT ---
if not exist .git (
    echo 🔧 Este parece ser o primeiro envio. Inicializando o repositório...
    git init
    echo.
    
    :GET_URL
    set "repo_url="
    set /p repo_url="🔗 Cole a URL do seu repositório GitHub aqui: "
    if not defined repo_url (
        echo ❌ A URL não pode estar vazia. Tente novamente.
        goto GET_URL
    )
    
    echo 🔄 Adicionando o repositório remoto...
    git remote add origin !repo_url!
    if %errorlevel% neq 0 (
        echo ⚠️  O repositório remoto 'origin' já existe. Tentando usar o existente...
        git remote set-url origin !repo_url!
    )
    echo.
) else (
    echo ✅ Repositório Git já configurado.
    echo.
)

REM --- 4. OBTER MENSAGEM DO COMMIT ---
:GET_COMMIT_MSG
set "commit_msg="
set /p commit_msg="📝 Digite uma mensagem para este envio (ex: Atualizando arquivos): "
if not defined commit_msg (
    echo ❌ A mensagem não pode estar vazia.
    goto GET_COMMIT_MSG
)
echo.

REM --- 5. EXECUTAR OS COMANDOS GIT ---
echo 📦 Adicionando todos os arquivos para o envio...
git add .

echo 💬 Criando o 'commit' com a mensagem: "!commit_msg!"
git commit -m "!commit_msg!"

REM Garante que a branch principal se chame 'main'
echo 🌿 Renomeando a branch para 'main' (padrão do GitHub)...
git branch -M main

echo.
echo 🚀 Enviando arquivos para o GitHub...
echo    (Pode ser que uma janela de login do GitHub apareça)
echo ──────────────────────────────────────────────────────────────

git push -u origin main

echo ──────────────────────────────────────────────────────────────
echo.

if %errorlevel%==0 (
    echo ✅ SUCESSO! Seus arquivos foram enviados para o GitHub.
) else (
    echo ❌ FALHA! Ocorreu um erro durante o envio.
    echo    Verifique a mensagem de erro acima.
    echo    Causas comuns: URL do repositório incorreta, falta de permissão ou conflitos.
)

echo.
pause
exit