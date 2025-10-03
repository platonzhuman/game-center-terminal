"""
Улучшенные крестики-нолики с ИИ и анимациями
"""

import curses
import random
import time

class TicTacToeGame:
    def __init__(self, stdscr, game_manager):
        self.stdscr = stdscr
        self.manager = game_manager
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.game_mode = 1  # 1 - против ИИ, 2 - два игрока
        self.difficulty = 2  # 1-легкий, 2-средний, 3-сложный, 4-нереальный
        self.game_over = False
        self.player_score = 0
        self.ai_score = 0
    
    def run(self):
        """Главный игровой цикл"""
        self.show_difficulty_menu()
        
        while not self.game_over:
            self.stdscr.clear()
            self.draw_board()
            self.draw_info()
            
            if self.game_mode == 1 and self.current_player == 'O':
                # Ход ИИ с анимацией
                self.stdscr.addstr(18, 2, "🤖 ИИ думает...", curses.color_pair(5))
                self.stdscr.refresh()
                time.sleep(0.5)
                
                move = self.get_ai_move()
                if move is not None:
                    self.animate_move(move, 'O')
                    self.board[move] = 'O'
                    if self.check_win('O'):
                        self.ai_score += 1
                        self.show_winner('O')
                    elif self.check_draw():
                        self.show_draw()
                    else:
                        self.current_player = 'X'
            else:
                # Ход человека
                move = self.get_human_move()
                if move is not None:
                    self.animate_move(move, 'X')
                    self.board[move] = self.current_player
                    if self.check_win(self.current_player):
                        self.player_score += 1
                        self.show_winner(self.current_player)
                    elif self.check_draw():
                        self.show_draw()
                    else:
                        self.current_player = 'O' if self.current_player == 'X' else 'X'
                elif move is None:  # ESC pressed
                    break
    
    def show_difficulty_menu(self):
        """Меню выбора сложности"""
        difficulties = [
            "🟢 Легкий - ИИ ходит случайно",
            "🟡 Средний - ИИ блокирует ходы", 
            "🟠 Сложный - ИИ использует стратегию",
            "🔴 Нереальный - ИИ непобедим",
            "👥 Игра с другом"
        ]
        
        current_choice = 1
        
        while True:
            self.stdscr.clear()
            height, width = self.stdscr.getmaxyx()
            
            title = "🎯 ВЫБЕРИТЕ СЛОЖНОСТЬ"
            self.stdscr.addstr(2, (width - len(title)) // 2, title, curses.color_pair(1) | curses.A_BOLD)
            
            for i, diff in enumerate(difficulties):
                y = 5 + i * 2
                x = (width - len(diff)) // 2
                
                if i == current_choice:
                    self.stdscr.addstr(y, x - 2, f"> {diff} <", curses.color_pair(2) | curses.A_BOLD)
                else:
                    self.stdscr.addstr(y, x, diff, curses.color_pair(1))
            
            self.stdscr.refresh()
            key = self.stdscr.getch()
            
            if key == curses.KEY_UP and current_choice > 0:
                current_choice -= 1
            elif key == curses.KEY_DOWN and current_choice < len(difficulties) - 1:
                current_choice += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if current_choice == 4:  # Игра с другом
                    self.game_mode = 2
                else:
                    self.game_mode = 1
                    self.difficulty = current_choice + 1
                break
            elif key == 27:
                self.game_over = True
                return
    
    def animate_move(self, position, player):
        """Анимация хода"""
        row = position // 3
        col = position % 3
        y = 5 + row * 2
        x = (self.stdscr.getmaxyx()[1] - 11) // 2 + col * 4
        
        symbols = ['•', '○', '●'] if player == 'O' else ['+', '×', 'X']
        
        for symbol in symbols:
            self.stdscr.addstr(y, x, f" {symbol} ", curses.color_pair(6 if player == 'O' else 4))
            self.stdscr.refresh()
            time.sleep(0.1)
    
    def draw_board(self):
        """Отрисовка игрового поля"""
        height, width = self.stdscr.getmaxyx()
        
        title = "🎯 КРЕСТИКИ-НОЛИКИ PRO"
        self.stdscr.addstr(2, (width - len(title)) // 2, title, curses.color_pair(1) | curses.A_BOLD)
        
        # Рисуем поле
        board_width = 11
        start_x = (width - board_width) // 2
        
        for i in range(3):
            y = 5 + i * 2
            for j in range(3):
                cell_index = i * 3 + j
                cell_value = self.board[cell_index]
                x = start_x + j * 4
                
                if cell_value == 'X':
                    self.stdscr.addstr(y, x, f" {cell_value} ", curses.color_pair(4) | curses.A_BOLD)
                elif cell_value == 'O':
                    self.stdscr.addstr(y, x, f" {cell_value} ", curses.color_pair(6) | curses.A_BOLD)
                else:
                    self.stdscr.addstr(y, x, f" {cell_index + 1} ", curses.color_pair(3))
                
                if j < 2:
                    self.stdscr.addstr(y, x + 3, "│", curses.color_pair(3))
            
            if i < 2:
                separator = "───┼───┼───"
                self.stdscr.addstr(y + 1, start_x, separator, curses.color_pair(3))
    
    def draw_info(self):
        """Отрисовка информации о игре"""
        height, width = self.stdscr.getmaxyx()
        
        mode_text = "🤖 Против ИИ" if self.game_mode == 1 else "👥 Два игрока"
        difficulty_names = ["", "Легкий", "Средний", "Сложный", "Нереальный"]
        difficulty_text = f"Сложность: {difficulty_names[self.difficulty]}" if self.game_mode == 1 else ""
        player_text = f"Текущий игрок: {self.current_player}"
        score_text = f"Счет: Вы {self.player_score} - {self.ai_score} ИИ"
        
        self.stdscr.addstr(12, 2, mode_text, curses.color_pair(1))
        if self.game_mode == 1:
            self.stdscr.addstr(13, 2, difficulty_text, curses.color_pair(1))
        self.stdscr.addstr(14, 2, player_text, curses.color_pair(2))
        self.stdscr.addstr(15, 2, score_text, curses.color_pair(3))
        self.stdscr.addstr(17, 2, "Управление: 1-9 - ход, ESC - выход", curses.color_pair(5))
    
    def get_human_move(self):
        """Получить ход от человека"""
        height, width = self.stdscr.getmaxyx()
        
        while True:
            self.stdscr.addstr(19, 2, "Ваш ход (1-9): ", curses.color_pair(3))
            self.stdscr.refresh()
            
            key = self.stdscr.getch()
            
            if key == 27:  # ESC
                return None
            elif 49 <= key <= 57:  # Клавиши 1-9
                move = key - 49
                if 0 <= move <= 8 and self.board[move] == ' ':
                    return move
                else:
                    self.stdscr.addstr(20, 2, "Неверный ход! Попробуйте снова.", curses.color_pair(4))
                    self.stdscr.refresh()
                    time.sleep(1)
                    self.stdscr.addstr(20, 2, " " * 40)  # Очистка строки
            else:
                self.stdscr.addstr(20, 2, "Нажмите цифру от 1 до 9!", curses.color_pair(4))
                self.stdscr.refresh()
                time.sleep(1)
                self.stdscr.addstr(20, 2, " " * 40)  # Очистка строки
    
    def get_ai_move(self):
        """Ход искусственного интеллекта"""
        # Легкий уровень - случайные ходы
        if self.difficulty == 1:
            empty_cells = [i for i, cell in enumerate(self.board) if cell == ' ']
            return random.choice(empty_cells) if empty_cells else None
        
        # Средний уровень - базовая стратегия
        elif self.difficulty == 2:
            # Пробуем выиграть
            for i in range(9):
                if self.board[i] == ' ':
                    self.board[i] = 'O'
                    if self.check_win('O'):
                        self.board[i] = ' '
                        return i
                    self.board[i] = ' '
            
            # Блокируем игрока
            for i in range(9):
                if self.board[i] == ' ':
                    self.board[i] = 'X'
                    if self.check_win('X'):
                        self.board[i] = ' '
                        return i
                    self.board[i] = ' '
            
            # Случайный ход
            empty_cells = [i for i, cell in enumerate(self.board) if cell == ' ']
            return random.choice(empty_cells) if empty_cells else None
        
        # Сложный уровень - улучшенная стратегия
        elif self.difficulty == 3:
            # Центр
            if self.board[4] == ' ':
                return 4
            
            # Углы
            corners = [0, 2, 6, 8]
            empty_corners = [c for c in corners if self.board[c] == ' ']
            if empty_corners:
                return random.choice(empty_corners)
            
            # Стороны
            sides = [1, 3, 5, 7]
            empty_sides = [s for s in sides if self.board[s] == ' ']
            if empty_sides:
                return random.choice(empty_sides)
            
            return None
        
        # Нереальный уровень - минимакс
        else:
            best_score = -float('inf')
            best_move = None
            
            for i in range(9):
                if self.board[i] == ' ':
                    self.board[i] = 'O'
                    score = self.minimax(0, False)
                    self.board[i] = ' '
                    
                    if score > best_score:
                        best_score = score
                        best_move = i
            
            return best_move
    
    def minimax(self, depth, is_maximizing):
        """Алгоритм минимакс"""
        if self.check_win('O'):
            return 1
        if self.check_win('X'):
            return -1
        if self.check_draw():
            return 0
        
        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if self.board[i] == ' ':
                    self.board[i] = 'O'
                    score = self.minimax(depth + 1, False)
                    self.board[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if self.board[i] == ' ':
                    self.board[i] = 'X'
                    score = self.minimax(depth + 1, True)
                    self.board[i] = ' '
                    best_score = min(score, best_score)
            return best_score
    
    def check_win(self, player):
        """Проверка победы"""
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Горизонтали
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Вертикали
            [0, 4, 8], [2, 4, 6]              # Диагонали
        ]
        
        for combo in win_combinations:
            if all(self.board[i] == player for i in combo):
                return True
        return False
    
    def check_draw(self):
        """Проверка ничьи"""
        return ' ' not in self.board
    
    def show_winner(self, player):
        """Показать победителя"""
        height, width = self.stdscr.getmaxyx()
        
        self.stdscr.clear()
        self.draw_board()
        
        if player == 'X':
            message = "🎉 ПОБЕДА! Вы выиграли!"
            color = curses.color_pair(3)
        else:
            message = "🤖 ИИ победил! Попробуйте снова!"
            color = curses.color_pair(4)
        
        self.stdscr.addstr(12, (width - len(message)) // 2, message, color | curses.A_BOLD)
        
        # Анимация победы
        for i in range(3):
            self.stdscr.addstr(14, (width - 20) // 2, "Нажмите любую клавишу...", curses.color_pair(2 if i % 2 == 0 else 1))
            self.stdscr.refresh()
            time.sleep(0.3)
        
        self.stdscr.getch()
        self.reset_game()
    
    def show_draw(self):
        """Показать ничью"""
        height, width = self.stdscr.getmaxyx()
        
        self.stdscr.clear()
        self.draw_board()
        
        message = "🤝 НИЧЬЯ! Хорошая игра!"
        self.stdscr.addstr(12, (width - len(message)) // 2, message, curses.color_pair(2) | curses.A_BOLD)
        self.stdscr.addstr(14, (width - 20) // 2, "Нажмите любую клавишу...", curses.color_pair(1))
        self.stdscr.refresh()
        self.stdscr.getch()
        self.reset_game()
    
    def reset_game(self):
        """Сброс игры для нового раунда"""
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        # Не сбрасываем счетчики очков
