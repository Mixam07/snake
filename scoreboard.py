import pygame.font
from pygame.sprite import Group

from snake import Snake

class Scoreboard:
    """Клас, що виводить рахунок"""

    def __init__(self, snake_game):
        """Ініціалізація атрибутів, пов'язаних із рахунком"""
        self.snake_game = snake_game
        self.screen = snake_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = snake_game.settings

        #Налаштування шрифту для відображення рахунку
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #Підготувати зображення на початкового рахунку
        self.prep_score()

    def prep_score(self):
        """Перетворити рухунок на зображення"""
        score_str = str(self.snake_game.snake.number_parts)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        #Показати рахунок у верхньому правому куті екрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Намалювати на екрані рахунок"""
        self.screen.blit(self.score_image, self.score_rect)