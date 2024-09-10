import pygame
import math
import random
from pygame.sprite import Sprite

class Apple(Sprite):
    """Клас для керуванням яблуком"""
    def __init__(self, snake_game):
        """Ініціалізувати прибnльця та задати його початкове розташування"""
        super().__init__()
        self.screen = snake_game.screen
        self.settings = snake_game.settings
        self.screen_rect = snake_game.screen.get_rect()

        self.image = pygame.image.load('images/apple.bmp')
        self.image = pygame.transform.scale(self.image, (self.settings.size_snake, self.settings.size_snake))

        self.rect = self.image.get_rect()

        self.generate_position()

    def generate_position(self):
        """Згенерувати рандомно пизицію яблука"""
        number_rows = int(math.floor(self.screen_rect.right / self.settings.size_snake))
        number_columns = int(math.floor(self.screen_rect.bottom / self.settings.size_snake))

        random_row = random.randint(1, number_rows - 1)
        random_column = random.randint(1, number_columns - 1)

        self.rect.x = random_row * self.settings.size_snake
        self.rect.y = random_column * self.settings.size_snake

    def blitme(self):
        """Намалювати корабель у його поточному розташуванні"""
        self.screen.blit(self.image, self.rect)