"""
Классическая змейка с улучшенной графикой
"""

import curses
import random
import time
import collections

class SnakeGame:
    def __init__(self, stdscr, game_manager):
        self.stdscr = stdscr
        self.manager = game_manager
        self.score = 0
        self.high_score = self.manager.get_high_score('snake')
        self.snake = None
        self.food = None
        self.direction = curses.KEY_RIGHT
        self.next_direction = curses.KEY_RIGHT
        self.game_speed = 150  # ms
        self.running = False
        
        # Размеры игрового поля (меньше для безопасности)
        self.game_height = 20
        self.game_width = 40
    
    def run(self):
        """Главный игровой цикл змейки"""
        self.initialize_game()
        self.running = True
        
        while self.running:
            start_time = time.time()
            
            # Обработка ввода
            self.handle_input()
            
            # Обновление игры
            self.update()
            
            # Отрисовка
            self.draw()
            
            # Контроль FPS
            elapsed = time.time() - start_time
            sleep_time = max(0.001, self.game_speed / 1000.0 - elapsed)
            time.sleep(sleep_time)
    
    def initialize_game(self):
        """Инициализация игры"""
        # Инициализация змейки
        self.snake = collections.deque()
        start_y = self.game_height // 2
        start_x = self.game_width // 2
        for i in range(3):
            self.snake.append((start_y, start_x - i))
        
        self.direction = curses.KEY_RIGHT
        self.next_direction = curses.KEY_RIGHT
        self.score = 0
        self.game_speed = 150
        self.generate_food()
    
    def handle_input(self):
        """Обработка пользовательского ввода"""
        self.stdscr.nodelay(1)
        key = self.stdscr.getch()
        
        if key != -1:
            if key == curses.KEY_UP and self.direction != curses.KEY_DOWN:
                self.next_direction = curses.KEY_UP
            elif key == curses.KEY_DOWN and self.direction != curses.KEY_UP:
                self.next_direction = curses.KEY_DOWN
            elif key == curses.KEY_LEFT and self.direction != curses.KEY_RIGHT:
                self.next_direction = curses.KEY_LEFT
            elif key == curses.KEY_RIGHT and self.direction != curses.KEY_LEFT:
                self.next_direction = curses.KEY_RIGHT
            elif key == 27:  # ESC
                self.running = False
            elif key == ord('p') or key == ord('P'):  # Pause
                self.show_pause_screen()
    
    def update(self):
        """Обновление игрового состояния"""
        self.direction = self.next_direction
        
        # Получаем текущую голову
        head_y, head_x = self.snake[0]
        
        # Вычисляем новую позицию головы
        if self.direction == curses.KEY_UP:
            new_head = (head_y - 1, head_x)
        elif self.direction == curses.KEY_DOWN:
            new_head = (head_y + 1, head_x)
        elif self.direction == curses.KEY_LEFT:
            new_head = (head_y, head_x - 1)
        elif self.direction == curses.KEY_RIGHT:
            new_head = (head_y, head_x + 1)
        
        # Проверка столкновений с границами
        if (new_head[0] <= 0 or new_head[0] >= self.game_height + 1 or 
            new_head[1] <= 0 or new_head[1] >= self.game_width + 1):
            self.game_over()
            return
        
        # Проверка столкновения с собой
        if new_head in self.snake:
            self.game_over()
            return
        
        # Добавляем новую голову
        self.snake.appendleft(new_head)
        
        # Проверка съедания еды
        if new_head == self.food:
            self.score += 10
            self.generate_food()
            
            # Увеличиваем скорость каждые 50 очков
            if self.score % 50 == 0 and self.game_speed > 50:
                self.game_speed -= 10
        else:
            # Удаляем хвост, если не съели еду
            self.snake.pop()
    
    def generate_food(self):
        """Генерация новой еды"""
        while True:
            y = random.randint(1, self.game_height)
            x = random.randint(1, self.game_width)
            if (y, x) not in self.snake:
                self.food = (y, x)
                break
    
    def draw(self):
        """Отрисовка игры"""
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        
        # Проверяем размер терминала
        if height < 25 or width < 50:
            self.show_small_screen_error()
            return
        
        # Заголовок
        title = "🐍 ЗМЕЙКА CLASSIC"
        self.stdscr.addstr(1, (width - len(title)) // 2, title, curses.color_pair(3) | curses.A_BOLD)
        
        # Счет
        score_text = f"Счет: {self.score} | Рекорд: {self.high_score} | Скорость: {200 - self.game_speed}"
        self.stdscr.addstr(2, (width - len(score_text)) // 2, score_text, curses.color_pair(1))
        
        # Рисуем границы
        self.draw_borders()
        
        # Рисуем змейку
        for i, (y, x) in enumerate(self.snake):
            # Смещаем координаты для отрисовки внутри поля
            draw_y = y + 4
            draw_x = x + (width - self.game_width) // 2
            
            if i == 0:  # Голова
                self.stdscr.addstr(draw_y, draw_x, "●", curses.color_pair(2))
            else:  # Тело
                self.stdscr.addstr(draw_y, draw_x, "○", curses.color_pair(3))
        
        # Рисуем еду
        food_y = self.food[0] + 4
        food_x = self.food[1] + (width - self.game_width) // 2
        self.stdscr.addstr(food_y, food_x, "●", curses.color_pair(4))
        
        # Управление
        controls = "Управление: Стрелки - движение, P - пауза, ESC - выход"
        if height > 25:
            self.stdscr.addstr(25, (width - len(controls)) // 2, controls, curses.color_pair(5))
        
        self.stdscr.refresh()
    
    def draw_borders(self):
        """Отрисовка границ игрового поля"""
        height, width = self.stdscr.getmaxyx()
        start_x = (width - self.game_width) // 2
        
        # Верхняя граница
        top_y = 4
        for x in range(start_x, start_x + self.game_width + 2):
            if top_y < height and x < width:
                if x == start_x:
                    self.stdscr.addstr(top_y, x, "┌", curses.color_pair(1))
                elif x == start_x + self.game_width + 1:
                    self.stdscr.addstr(top_y, x, "┐", curses.color_pair(1))
                else:
                    self.stdscr.addstr(top_y, x, "─", curses.color_pair(1))
        
        # Боковые границы и нижняя граница
        bottom_y = 4 + self.game_height + 1
        for y in range(5, 5 + self.game_height + 1):
            if y < height:
                # Левая граница
                if start_x < width:
                    self.stdscr.addstr(y, start_x, "│", curses.color_pair(1))
                # Правая граница
                right_x = start_x + self.game_width + 1
                if right_x < width:
                    self.stdscr.addstr(y, right_x, "│", curses.color_pair(1))
        
        # Нижняя граница
        if bottom_y < height:
            for x in range(start_x, start_x + self.game_width + 2):
                if x < width:
                    if x == start_x:
                        self.stdscr.addstr(bottom_y, x, "└", curses.color_pair(1))
                    elif x == start_x + self.game_width + 1:
                        self.stdscr.addstr(bottom_y, x, "┘", curses.color_pair(1))
                    else:
                        self.stdscr.addstr(bottom_y, x, "─", curses.color_pair(1))
    
    def show_small_screen_error(self):
        """Показать ошибку маленького экрана"""
        height, width = self.stdscr.getmaxyx()
        message = "Слишком маленький терминал!"
        advice = "Увеличьте окно до 50x25 символов"
        self.stdscr.addstr(height//2 - 1, (width - len(message)) // 2, message, curses.color_pair(4))
        self.stdscr.addstr(height//2 + 1, (width - len(advice)) // 2, advice, curses.color_pair(1))
        self.stdscr.addstr(height//2 + 3, (width - 20) // 2, "Нажмите любую клавишу", curses.color_pair(2))
        self.stdscr.refresh()
        self.stdscr.getch()
        self.running = False
    
    def show_pause_screen(self):
        """Экран паузы"""
        height, width = self.stdscr.getmaxyx()
        
        pause_msg = "⏸️ ПАУЗА"
        continue_msg = "Нажмите P для продолжения"
        
        self.stdscr.addstr(height//2 - 1, (width - len(pause_msg)) // 2, pause_msg, curses.color_pair(2) | curses.A_BOLD)
        self.stdscr.addstr(height//2 + 1, (width - len(continue_msg)) // 2, continue_msg, curses.color_pair(1))
        self.stdscr.refresh()
        
        while True:
            key = self.stdscr.getch()
            if key == ord('p') or key == ord('P'):
                break
            elif key == 27:  # ESC
                self.running = False
                break
    
    def game_over(self):
        """Завершение игры"""
        # Сохраняем рекорд
        if self.score > self.high_score:
            self.manager.save_high_score('snake', self.score)
            new_record = True
        else:
            new_record = False
        
        height, width = self.stdscr.getmaxyx()
        
        # Анимация проигрыша
        for i in range(3):
            self.stdscr.clear()
            if i % 2 == 0:
                self.draw()
            
            message = "💀 ИГРА ОКОНЧЕНА!"
            if new_record:
                record_msg = "🎉 НОВЫЙ РЕКОРД!"
                self.stdscr.addstr(height//2 - 2, (width - len(record_msg)) // 2, record_msg, curses.color_pair(3) | curses.A_BOLD)
            
            self.stdscr.addstr(height//2, (width - len(message)) // 2, message, curses.color_pair(4) | curses.A_BOLD)
            
            score_text = f"Ваш счет: {self.score}"
            self.stdscr.addstr(height//2 + 1, (width - len(score_text)) // 2, score_text, curses.color_pair(1))
            
            high_score_text = f"Рекорд: {max(self.score, self.high_score)}"
            self.stdscr.addstr(height//2 + 2, (width - len(high_score_text)) // 2, high_score_text, curses.color_pair(2))
            
            continue_text = "Нажмите пробел для новой игры"
            self.stdscr.addstr(height//2 + 4, (width - len(continue_text)) // 2, continue_text, curses.color_pair(5))
            
            exit_text = "или ESC для выхода в меню"
            self.stdscr.addstr(height//2 + 5, (width - len(exit_text)) // 2, exit_text, curses.color_pair(5))
            
            self.stdscr.refresh()
            time.sleep(0.5)
        
        # Ожидание выбора игрока
        while True:
            key = self.stdscr.getch()
            if key == ord(' '):
                self.initialize_game()
                break
            elif key == 27:  # ESC
                self.running = False
                break
