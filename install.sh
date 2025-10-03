#!/bin/bash
# install.sh - Установочный скрипт для Linux/macOS

echo "🎮 Terminal Game Manager - Установка"
echo "====================================="

# Проверяем Python
if command -v python3 &> /dev/null; then
    echo "✅ Python найден: $(python3 --version)"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    echo "✅ Python найден: $(python --version)"
    PYTHON_CMD="python"
else
    echo "❌ Python не найден!"
    echo "Установи Python: https://python.org"
    exit 1
fi

# Создаем временную папку
TEMP_DIR="/tmp/terminal-game-manager"
mkdir -p "$TEMP_DIR"

cleanup() {
    echo "🧹 Убираю временные файлы..."
    rm -rf "$TEMP_DIR"
}

trap cleanup EXIT

echo ""
echo "📥 Скачиваю игру..."

# Скачиваем и распаковываем
if command -v curl &> /dev/null; then
    curl -L -o "$TEMP_DIR/game.zip" "https://github.com/platonzhuman/terminal-game-manager/archive/main.zip"
elif command -v wget &> /dev/null; then
    wget -O "$TEMP_DIR/game.zip" "https://github.com/platonzhuman/terminal-game-manager/archive/main.zip"
else
    echo "❌ Нужен curl или wget для скачивания"
    exit 1
fi

echo "📦 Распаковываю..."
unzip -q "$TEMP_DIR/game.zip" -d "$TEMP_DIR"

echo "📁 Копирую файлы..."
cp -r "$TEMP_DIR/terminal-game-manager-main/"* .

echo "✅ Установка завершена!"
echo ""
echo "🎮 Запускаю игру..."

# Запускаем игру
$PYTHON_CMD -m tgm.main
