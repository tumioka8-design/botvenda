@echo off
chcp 65001 >nul
title Bot Manager - Perky Logins Bot
color 0b
setlocal enabledelayedexpansion

REM Detectar comando Python disponível
set "PYTHON_CMD="
py --version >nul 2>&1
if %errorlevel%==0 (
    set "PYTHON_CMD=py"
) else (
    python --version >nul 2>&1
    if %errorlevel%==0 (
        set "PYTHON_CMD=python"
    ) else (
        echo.
        echo ❌ Python não encontrado! 
        echo 💡 Instale o Python em python.org
        pause
        exit /b 1
    )
)

REM Verificar se foi passado argumento (para execução direta)
if "%1" neq "" (
    set "choice=%1"
    goto PROCESS_CHOICE
)

:MENU
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    BOT MANAGER - PERKY LOGINS                ║
echo ╠══════════════════════════════════════════════════════════════╣
echo ║  Python detectado: %PYTHON_CMD%                                      ║
echo ║                                                              ║
echo ║  [1] 🚀 Iniciar Bot                                          ║
echo ║  [2] 🛑 Parar Bot                                            ║
echo ║  [3] 📊 Status do Bot                                        ║
echo ║  [4] 📋 Monitor (Ver logs em tempo real)                     ║
echo ║  [5] 🔄 Reiniciar Bot                                        ║
echo ║  [6] 📁 Abrir pasta do projeto                               ║
echo ║  [7] 🔧 Instalar/Atualizar dependências                     ║
echo ║  [8] 📝 Ver últimos logs                                     ║
echo ║  [9] 🧪 Testar bot (executar uma vez)                       ║
echo ║  [C] 🧹 Limpeza completa (resolver erro 409)                ║
echo ║  [0] ❌ Sair                                                 ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

set /p choice="Digite sua opção (0-9,C): "

:PROCESS_CHOICE
if "%choice%"=="1" goto START_BOT
if "%choice%"=="2" goto STOP_BOT
if "%choice%"=="3" goto STATUS_BOT
if "%choice%"=="4" goto MONITOR_BOT
if "%choice%"=="5" goto RESTART_BOT
if "%choice%"=="6" goto OPEN_FOLDER
if "%choice%"=="7" goto INSTALL_DEPS
if "%choice%"=="8" goto VIEW_LOGS
if "%choice%"=="9" goto TEST_BOT
if "%choice%"=="C" goto CLEANUP_COMPLETE
if "%choice%"=="c" goto CLEANUP_COMPLETE
if "%choice%"=="0" goto EXIT

REM Se foi executado com argumento e opção inválida
if "%1" neq "" (
    echo ❌ Opção inválida: %choice%
    echo 💡 Use: bot_manager.bat [1-9,0,C]
    exit /b 1
)

echo.
echo ❌ Opção inválida! Tente novamente.
timeout /t 2 >nul
call :RETURN_TO_MENU

:START_BOT
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                        INICIANDO BOT                         ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Verificar se o bot já está rodando
call :CHECK_BOT_RUNNING
if "!bot_running!"=="true" (
    echo ⚠️  Bot já está em execução!
    echo.
    pause
    call :RETURN_TO_MENU
)

echo 🚀 Iniciando o bot...
cd /d "%~dp0"

REM Verificar se o arquivo bot.py existe
if not exist "bot.py" (
    echo ❌ Arquivo bot.py não encontrado!
    echo 📁 Verifique se está na pasta correta.
    pause
    call :RETURN_TO_MENU
)

REM Verificar dependências
echo 📦 Verificando dependências...
%PYTHON_CMD% -c "import telebot, mercadopago, pytz" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Dependências não encontradas! Instalando...
    %PYTHON_CMD% -m pip install pyTelegramBotAPI mercadopago pytz
    if !errorlevel! neq 0 (
        echo ❌ Erro ao instalar dependências!
        pause
        call :RETURN_TO_MENU
    )
)

REM Iniciar o bot em background
echo 🔄 Executando bot.py...

REM Criar arquivo de log para capturar erros
set "LOG_FILE=%~dp0bot_error.log"
if exist "%LOG_FILE%" del "%LOG_FILE%"

REM Iniciar o bot usando PowerShell em background (sem janelas extras)
powershell -WindowStyle Hidden -Command "cd '%~dp0'; %PYTHON_CMD% bot.py 2>'%LOG_FILE%'" &
timeout /t 3 >nul

REM Verificar se o processo foi criado
call :CHECK_BOT_RUNNING
if "!bot_running!"=="true" (
    echo ✅ Bot iniciado com sucesso!
    echo 📱 Acesse: t.me/Perky_Logins_bot
    echo 🆔 PID do processo: !bot_pid!
    echo.
    echo 🧪 Testando conectividade com Telegram...
    %PYTHON_CMD% -c "import requests,json;config=json.load(open('settings/credenciais.json'));r=requests.get(f'https://api.telegram.org/bot{config[\"api-bot\"]}/getMe');print('✅ Bot conectado!' if r.status_code==200 and r.json()['ok'] else '❌ Erro de conectividade')" 2>nul || echo "⚠️ Teste falhou"
    echo.
    echo 🎯 STATUS: BOT ONLINE E FUNCIONANDO!
    echo 💡 Envie /start para @Perky_Logins_bot para testar
) else (
    echo ❌ Erro ao iniciar o bot!
    if exist "%LOG_FILE%" (
        echo 📋 Verificando erros...
        for %%A in ("%LOG_FILE%") do if %%~zA gtr 0 (
            echo.
            echo 🚨 ERRO ENCONTRADO:
            echo ────────────────────
            type "%LOG_FILE%"
            echo ────────────────────
        )
    )
    echo 💡 Use a opção [9] para testar e ver erros detalhados.
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo 📊 RESUMO: 
call :CHECK_BOT_RUNNING
if "!bot_running!"=="true" (
    echo    🟢 Status: ONLINE ^| PID: !bot_pid!
) else (
    echo    🔴 Status: OFFLINE
)
echo    🤖 Bot: @Perky_Logins_bot
echo    📱 Telegram: t.me/Perky_Logins_bot
echo ═══════════════════════════════════════════════════════════════

:START_BOT_MENU
echo.
echo O que deseja fazer agora?
echo [R] - Reiniciar o bot
echo [V] - Voltar ao menu principal
set /p start_choice="Digite sua opção (R/V): "

if /i "%start_choice%"=="R" goto RESTART_BOT
if /i "%start_choice%"=="V" goto RETURN_TO_MENU

echo.
echo ❌ Opção inválida!
goto START_BOT_MENU

:STOP_BOT
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                        PARANDO BOT                           ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🛑 Procurando processos do bot...

call :CHECK_BOT_RUNNING
if "!bot_running!"=="true" (
    echo 🔴 Parando processo !bot_pid!...
    taskkill /pid !bot_pid! /f >nul 2>&1
    if !errorlevel!==0 (
        echo ✅ Bot parado com sucesso!
    ) else (
        echo ⚠️  Erro ao parar o processo !bot_pid!
    )
) else (
    echo ⚠️  Nenhum processo do bot encontrado.
)

echo.
pause
call :RETURN_TO_MENU

:STATUS_BOT
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                        STATUS DO BOT                         ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🔍 Verificando status...
echo.

call :CHECK_BOT_RUNNING
if "!bot_running!"=="true" (
    echo ✅ Bot Status: ONLINE
    echo 🆔 PID: !bot_pid!
    echo 📱 Bot: t.me/Perky_Logins_bot
    echo 🐍 Python: %PYTHON_CMD%
    echo ⏰ Verificado em: !date! !time!
) else (
    echo ❌ Bot Status: OFFLINE
    echo 📱 Bot: t.me/Perky_Logins_bot
    echo 🐍 Python: %PYTHON_CMD%
    echo ⏰ Verificado em: !date! !time!
)

echo.
pause
call :RETURN_TO_MENU

:MONITOR_BOT
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    MONITOR DO BOT                            ║
echo ║              (Pressione Ctrl+C para sair)                   ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 📊 Monitorando bot em tempo real...
echo 🔄 Atualizando a cada 5 segundos...
echo.

:MONITOR_LOOP
call :CHECK_BOT_RUNNING
if "!bot_running!"=="true" (
    echo [!time!] ✅ Bot ONLINE - PID: !bot_pid!
) else (
    echo [!time!] ❌ Bot OFFLINE
)

timeout /t 5 >nul
goto MONITOR_LOOP

:RESTART_BOT
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                      REINICIANDO BOT                         ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🔄 Reiniciando o bot...
echo.

echo 🛑 Parando bot atual...
call :CHECK_BOT_RUNNING
if "!bot_running!"=="true" (
    taskkill /pid !bot_pid! /f >nul 2>&1
)

timeout /t 2 >nul

echo 🚀 Iniciando bot novamente...
cd /d "%~dp0"

REM Criar arquivo de log para capturar erros
set "LOG_FILE=%~dp0bot_error.log"
if exist "%LOG_FILE%" del "%LOG_FILE%"

REM Iniciar o bot usando PowerShell em background (sem janelas extras)
powershell -WindowStyle Hidden -Command "cd '%~dp0'; %PYTHON_CMD% bot.py 2>'%LOG_FILE%'" &
timeout /t 3 >nul

call :CHECK_BOT_RUNNING
if "!bot_running!"=="true" (
    echo ✅ Bot reiniciado com sucesso!
    echo 🆔 PID: !bot_pid!
) else (
    echo ❌ Erro ao reiniciar o bot!
    if exist "%LOG_FILE%" (
        for %%A in ("%LOG_FILE%") do if %%~zA gtr 0 (
            echo.
            echo 🚨 ERRO:
            type "%LOG_FILE%"
        )
    )
)
echo.
pause
call :RETURN_TO_MENU

:TEST_BOT
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                      TESTANDO BOT                            ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🧪 Executando bot em modo teste...
echo 👀 Você verá qualquer erro que ocorrer:
echo.

cd /d "%~dp0"
%PYTHON_CMD% bot.py
echo.
echo 🔚 Teste finalizado.
pause
call :RETURN_TO_MENU

:OPEN_FOLDER
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    ABRINDO PASTA                             ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 📁 Abrindo pasta do projeto...
explorer "%~dp0"
timeout /t 1 >nul
call :RETURN_TO_MENU

:INSTALL_DEPS
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                 INSTALANDO DEPENDÊNCIAS                      ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 📦 Instalando/Atualizando dependências...
echo.

cd /d "%~dp0"

if exist requirements.txt (
    echo 🔧 Instalando a partir do requirements.txt...
    %PYTHON_CMD% -m pip install -r requirements.txt
) else (
    echo 🔧 Instalando dependências principais...
    %PYTHON_CMD% -m pip install pyTelegramBotAPI mercadopago pytz
)

echo.
if %errorlevel%==0 (
    echo ✅ Dependências instaladas com sucesso!
) else (
    echo ❌ Erro ao instalar dependências!
)
echo.
pause
call :RETURN_TO_MENU

:VIEW_LOGS
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                      ÚLTIMOS LOGS                            ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

if exist "log\compra.txt" (
    echo 🛒 ÚLTIMAS COMPRAS:
    echo ────────────────────
    type "log\compra.txt" | more
    echo.
)

if exist "log\recarga.txt" (
    echo 💰 ÚLTIMAS RECARGAS:
    echo ────────────────────
    type "log\recarga.txt" | more
    echo.
)

if exist "log\registro.txt" (
    echo 👤 ÚLTIMOS REGISTROS:
    echo ────────────────────
    type "log\registro.txt" | more
    echo.
)

echo.
pause
call :RETURN_TO_MENU

:CHECK_BOT_RUNNING
set "bot_running=false"
set "bot_pid="

REM Procurar por python.exe
for /f "tokens=2" %%i in ('tasklist /fi "imagename eq python.exe" /fo list 2^>nul ^| findstr "PID"') do (
    wmic process where "ProcessId=%%i" get CommandLine /format:list 2>nul | findstr "bot.py" >nul
    if !errorlevel!==0 (
        set "bot_running=true"
        set "bot_pid=%%i"
        goto :eof
    )
)

REM Procurar por py.exe (Python Launcher)
for /f "tokens=2" %%i in ('tasklist /fi "imagename eq py.exe" /fo list 2^>nul ^| findstr "PID"') do (
    wmic process where "ProcessId=%%i" get CommandLine /format:list 2>nul | findstr "bot.py" >nul
    if !errorlevel!==0 (
        set "bot_running=true"
        set "bot_pid=%%i"
        goto :eof
    )
)

REM Procurar por cmd.exe que executa bot.py
for /f "tokens=2" %%i in ('tasklist /fi "imagename eq cmd.exe" /fo list 2^>nul ^| findstr "PID"') do (
    wmic process where "ProcessId=%%i" get CommandLine /format:list 2>nul | findstr "bot.py" >nul
    if !errorlevel!==0 (
        set "bot_running=true"
        set "bot_pid=%%i"
        goto :eof
    )
)

REM Procurar por powershell.exe que executa bot.py
for /f "tokens=2" %%i in ('tasklist /fi "imagename eq powershell.exe" /fo list 2^>nul ^| findstr "PID"') do (
    wmic process where "ProcessId=%%i" get CommandLine /format:list 2>nul | findstr "bot.py" >nul
    if !errorlevel!==0 (
        set "bot_running=true"
        set "bot_pid=%%i"
        goto :eof
    )
)
goto :eof

:CLEANUP_COMPLETE
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    LIMPEZA COMPLETA DO BOT                   ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🧹 Parando TODOS os processos Python...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im py.exe >nul 2>&1
echo ✅ Processos Python parados

echo.
echo 🔄 Limpando possíveis arquivos temporários...
if exist "bot_error.log" del "bot_error.log"
echo ✅ Arquivos temporários limpos

echo.
echo 🕐 Aguardando 15 segundos para o Telegram liberar o token...
echo    (Isso resolve o erro 409 - Conflict)

for /l %%i in (15,-1,1) do (
    echo ⏳ Aguardando %%i segundos...
    timeout /t 1 >nul
)

echo.
echo ✅ Limpeza concluída! O bot deve funcionar agora.
echo 💡 Use a opção [1] para iniciar o bot.
echo.
pause
call :RETURN_TO_MENU

:RETURN_TO_MENU
if "%1" neq "" (
    REM Se foi executado com argumento, sair
    exit /b 0
) else (
    REM Se foi executado interativamente, voltar ao menu
    goto MENU
)

:EXIT
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                         SAINDO                               ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 👋 Obrigado por usar o Bot Manager!
echo 🤖 Seu bot: t.me/Perky_Logins_bot
echo.
timeout /t 2 >nul
exit
