"""
Менеджер игр и системы сохранений
"""

import json
import os
from pathlib import Path

class GameManager:
    def __init__(self):
        self.config_dir = Path.home() / '.terminal_games'
        self.scores_file = self.config_dir / 'scores.json'
        self.config_dir.mkdir(exist_ok=True)
    
    def get_high_score(self, game_name):
        """Получить рекорд для игры"""
        try:
            if self.scores_file.exists():
                with open(self.scores_file, 'r') as f:
                    scores = json.load(f)
                    return scores.get(game_name, 0)
        except:
            pass
        return 0
    
    def save_high_score(self, game_name, score):
        """Сохранить новый рекорд"""
        try:
            scores = {}
            if self.scores_file.exists():
                with open(self.scores_file, 'r') as f:
                    scores = json.load(f)
            
            current_high = scores.get(game_name, 0)
            if score > current_high:
                scores[game_name] = score
                with open(self.scores_file, 'w') as f:
                    json.dump(scores, f, indent=2)
                return True
        except:
            pass
        return False
