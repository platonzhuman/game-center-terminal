"""
Анимации для игр
"""

import curses
import time

def startup_animation(stdscr):
    """Загрузочная анимация"""
    height, width = stdscr.getmaxyx()
    
    messages = [
        "🎮 Запуск Terminal Game Manager...",
        "📦 Загрузка игр...", 
        "🎨 Инициализация графики...",
        "🚀 Почти готово..."
    ]
    
    for i, message in enumerate(messages):
        stdscr.clear()
        stdscr.addstr(height//2 - 2, (width - len(message)) // 2, message, curses.A_BOLD)
        
        # Прогресс-бар
        progress = (i + 1) * 25
        bar = "[" + "█" * (progress // 5) + " " * (20 - progress // 5) + "]"
        stdscr.addstr(height//2, (width - len(bar)) // 2, bar)
        
        stdscr.refresh()
        time.sleep(0.5)
    
    stdscr.clear()
    stdscr.refresh()
