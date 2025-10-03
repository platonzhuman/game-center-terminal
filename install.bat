@echo off
chcp 65001 > nul
echo 🎮 Terminal Game Manager - Установка
echo =====================================

:: Проверяем Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python не найден!
    echo Скачай Python с: https://python.org
    pause
    exit /b 1
)

echo ✅ Python найден
echo.
echo 📥 Скачиваю игру...

:: Скачиваем через PowerShell
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/platonzhuman/terminal-game-manager/archive/main.zip' -OutFile 'game.zip'"

echo 📦 Распаковываю...
powershell -Command "Expand-Archive -Path 'game.zip' -DestinationPath '.' -Force"

echo 📁 Копирую файлы...
xcopy /E /I "terminal-game-manager-main\*" "."

echo ✅ Установка завершена!
echo.
echo 🎮 Запускаю игру...
python -m tgm.main

pause
