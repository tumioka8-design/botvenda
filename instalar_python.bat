@echo off
chcp 65001 >nul
title Instalador Python - Bot Manager
color 0e

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                   INSTALADOR PYTHON                          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🐍 Verificando Python...

REM Tentar python normal
python --version >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Python já está instalado!
    python --version
    echo.
    pause
    goto END
)

REM Tentar py launcher
py --version >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Python Launcher encontrado!
    py --version
    echo.
    echo 💡 Use 'py' em vez de 'python' nos comandos.
    pause
    goto END
)

echo ❌ Python não encontrado!
echo.
echo 📥 Baixando Python 3.11...
echo    Aguarde, isso pode demorar alguns minutos...

REM Criar diretório temporário
if not exist temp mkdir temp
cd temp

REM Baixar Python usando PowerShell
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile 'python_installer.exe'}"

if not exist python_installer.exe (
    echo ❌ Erro ao baixar Python!
    echo.
    echo 💡 Soluções:
    echo    1. Verifique sua conexão com a internet
    echo    2. Baixe manualmente: https://python.org/downloads
    echo    3. Instale Python 3.11 ou superior
    echo.
    pause
    cd ..
    goto END
)

echo ✅ Download concluído!
echo 🔧 Instalando Python...
echo    Por favor, aguarde...

REM Instalar Python silenciosamente
python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_tcltk=0

echo.
echo ⏳ Aguardando instalação terminar...
timeout /t 10 >nul

REM Limpeza
del python_installer.exe
cd ..
rmdir temp

echo.
echo ✅ Instalação concluída!
echo.
echo 🔄 IMPORTANTE: Feche e abra um novo terminal para usar o Python.
echo 📝 Teste com: python --version
echo.

:END
pause