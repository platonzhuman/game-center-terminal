"""
Базовый класс для всех игр в системе.
"""

from abc import ABC, abstractmethod
import curses

class BaseGame(ABC):
    """Абстрактный базовый класс для игр."""
    
    def __init__(self, stdscr, game_manager):
        self.stdscr = stdscr
        self.manager = game_manager
        self.name = "Без названия"
        self.description = "Описание игры"
        self.running = False
    
    @abstractmethod
    def run(self):
        """Основной игровой цикл."""
        pass
    
    @abstractmethod
    def draw(self):
        """Отрисовка игры."""
        pass
    
    def handle_input(self):
        """Обработка пользовательского ввода."""
        pass
    
    def show_game_over(self, message: str):
        """Показывает экран завершения игры."""
        height, width = self.stdscr.getmaxyx()
        
        # Анимация проигрыша
        for i in range(5):
            self.stdscr.clear()
            self.draw()
            
            color = curses.color_pair(2 if i % 2 == 0 else 4)
            self.stdscr.addstr(height//2, (width-len(message))//2, message, color)
            self.stdscr.refresh()
            curses.napms(300)
        
        self.stdscr.addstr(height//2 + 2, (width-20)//2, "Нажмите любую клавишу...")
        self.stdscr.refresh()
        self.stdscr.getch()
