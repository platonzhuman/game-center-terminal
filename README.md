# 🎮 Terminal Game Manager

**Установка одной командой для любой ОС!** Просто скопируй и вставь в терминал.

## 🚀 БЫСТРАЯ УСТАНОВКА

### Для Windows (PowerShell):
```powershell
irm https://raw.githubusercontent.com/platonzhuman/terminal-game-manager/main/install.ps1 | iex

Для Linux/macOS:
bash

curl -s https://raw.githubusercontent.com/platonzhuman/terminal-game-manager/main/install.sh | bash

Альтернатива для всех ОС (если выше не работает):
bash

# Скачай и запусти вручную
git clone https://github.com/platonzhuman/terminal-game-manager.git
cd terminal-game-manager
python -m tgm.main

🎮 ЗАПУСК ИГРЫ

После установки просто введи:
bash

tgm

ИЛИ если команда не найдена:
bash

python -m tgm.main

🎯 ЧТО ВНУТРИ:

    🎯 Крестики-нолики Pro с ИИ 4-х уровней сложности

    🐍 Классическая змейка с системой рекордов

    🎨 Красивый интерфейс с анимациями

    💾 Автосохранение прогресса

🛠️ РУЧНАЯ УСТАНОВКА
Windows:
powershell

# Скачай архив
Invoke-WebRequest -Uri "https://github.com/platonzhuman/terminal-game-manager/archive/main.zip" -OutFile "game.zip"
# Распакуй
Expand-Archive -Path "game.zip" -DestinationPath "."
cd terminal-game-manager-main
# Запусти
python -m tgm.main

Linux/macOS:
bash

wget https://github.com/platonzhuman/terminal-game-manager/archive/main.zip
unzip main.zip
cd terminal-game-manager-main
python3 -m tgm.main

❗ ЕСЛИ ВОЗНИКЛИ ПРОБЛЕМЫ:

    Убедись что Python установлен:
    bash

python --version

Должно быть 3.7 или выше

Если python не работает, попробуй:
bash

python3 --version

или на Windows:
powershell

py --version

    Нет интернета? Скачай ZIP вручную с GitHub и запусти python -m tgm.main

🎮 УПРАВЛЕНИЕ:

    Стрелки ↑↓ - навигация

    Enter - выбор

    ESC - выход

    Цифры 1-9 - ход в крестиках-ноликах

    Стрелки - управление змейкой

⭐ Нравится проект? Поставь звезду на GitHub!
