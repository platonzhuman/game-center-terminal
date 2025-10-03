#!/usr/bin/env python3
"""
Главный файл запуска Terminal Game Manager
"""

import curses
import sys

def main(stdscr=None):
    try:
        if stdscr is None:
            curses.wrapper(_main_internal)
        else:
            _main_internal(stdscr)
    except KeyboardInterrupt:
        print("\nДо свидания! Спасибо за игру!")
        sys.exit(0)

def _main_internal(stdscr):
    # Настройка curses
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.noecho()
    curses.cbreak()
    
    # Инициализация цветов
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)
    
    # Запуск главного меню
    from tgm.game_manager import GameManager
    manager = GameManager()
    
    # Главный цикл приложения
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Анимированный заголовок
        title = "🎮 ТЕРМИНАЛЬНЫЙ ИГРОВОЙ МЕНЕДЖЕР"
        stdscr.addstr(2, (width - len(title)) // 2, title, curses.color_pair(1) | curses.A_BOLD)
        
        # Меню выбора игры
        options = [
            "🎯 Крестики-Нолики Pro",
            "🐍 Змейка Classic", 
            "🚪 Выход"
        ]
        
        current_choice = 0
        
        while True:
            # Отрисовка меню
            for i, option in enumerate(options):
                y_pos = 5 + i * 2
                x_pos = (width - len(option)) // 2
                
                if i == current_choice:
                    stdscr.addstr(y_pos, x_pos - 2, f"> {option} <", curses.color_pair(2) | curses.A_BOLD)
                else:
                    stdscr.addstr(y_pos, x_pos, option, curses.color_pair(1))
            
            stdscr.refresh()
            
            # Обработка ввода
            key = stdscr.getch()
            
            if key == curses.KEY_UP and current_choice > 0:
                current_choice -= 1
            elif key == curses.KEY_DOWN and current_choice < len(options) - 1:
                current_choice += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if current_choice == 0:  # Крестики-нолики
                    from tgm.games.tic_tac_toe import TicTacToeGame
                    game = TicTacToeGame(stdscr, manager)
                    game.run()
                elif current_choice == 1:  # Змейка
                    from tgm.games.snake import SnakeGame
                    game = SnakeGame(stdscr, manager)
                    game.run()
                elif current_choice == 2:  # Выход
                    return
                break
            elif key == 27:  # ESC
                return

if __name__ == "__main__":
    main()
