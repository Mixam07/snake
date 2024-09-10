import pygame
import math
from pygame.sprite import Sprite

class Snake(Sprite):
    """Клас для керування змійкою"""
    def __init__(self, snake_game):
        """Ініціалізувати змійку і встановіть його вихідне положення"""
        super().__init__()
        self.screen = snake_game.screen
        self.settings = snake_game.settings
        self.screen_rect = snake_game.screen.get_rect()

        #Позиція головної точки
        self.rect = {
            "x": 0,
            "y": 0
        }

        self.color = (80, 200, 120)

        #Індикатор руху
        self.moving_direction = "top"

        #Налаштування змійки
        self.number_parts = self.settings.start_number_parts
        self.parts_list = []

        self.center_snake()
        self.init_snake()

    def update(self):
        """Оновити поточну позицію змійки на основі індикаторі руху"""
        screen_rect = self.screen.get_rect()

        #Оновити значення snike.x snike.y, а не rect
        if self.moving_direction == "top" and screen_rect.top <= self.parts_list[0]["position"]["y"]:
            self.y -= self.settings.snake_speed
        elif self.moving_direction == "right" and screen_rect.right + self.settings.size_snake * 2 >= self.parts_list[0]["position"]["x"]:
            self.x += self.settings.snake_speed
        elif self.moving_direction == "left" and screen_rect.left <= self.parts_list[0]["position"]["x"]:
            self.x -= self.settings.snake_speed
        elif self.moving_direction == "bottom" and screen_rect.bottom + self.settings.size_snake * 2 >= self.parts_list[0]["position"]["y"]:
            self.y += self.settings.snake_speed

        #Оновити об'єкт rect з self.x
        self.rect["x"] = int(self.x)
        self.rect["y"] = int(self.y)

        #Оновити список змійки
        self._update_snake()


    def init_snake(self):
        """Створення нової змійки"""
        self.parts_list = []

        for i in range(self.number_parts):
            self.parts_list.append({
                "position": {
                    "x": self.rect["x"],
                    "y": self.rect["y"] + self.settings.size_snake * i
                }
            })
        
    def _update_snake(self):
        """Оновити позицію змійки"""
        if(self.rect["y"] <= self.parts_list[0]["position"]["y"] - self.settings.size_snake and self.moving_direction == "top" or
            self.rect["x"] >= self.parts_list[0]["position"]["x"] + self.settings.size_snake and self.moving_direction == "right" or
            self.rect["x"] <= self.parts_list[0]["position"]["x"] - self.settings.size_snake and self.moving_direction == "left" or
            self.rect["y"] >= self.parts_list[0]["position"]["y"]  + self.settings.size_snake and self.moving_direction == "bottom"):

            rect = pygame.draw.rect(self.screen, self.color, (self.rect["x"], self.rect["y"], self.settings.size_snake, self.settings.size_snake))

            self.parts_list.insert(0, {
                "position": {
                    "x": self.rect["x"],
                    "y": self.rect["y"]
                }
            })

            self.parts_list = self.parts_list[:self.number_parts]

    def center_snake(self):
        """Відцентрувати корабель на екрані"""
        screen_rect = self.screen.get_rect()

        #Шукаю цент по осі x
        number_rows = screen_rect.right / self.settings.size_snake
        center_row = int(math.floor(number_rows / 2))

        #Створювати кожен нову змійку внизу екрану, по центру
        self.rect["y"] = screen_rect.bottom - self.settings.size_snake
        self.rect["x"] = center_row * self.settings.size_snake

        #Зберегти десяткове значення для позиції змійки
        self.x = float(self.rect["x"])
        self.y = float(self.rect["y"])

    def blitme(self):
        """Намалювати змійку у її поточному розташуванні"""
        i = 0

        for item in self.parts_list:
            rect = pygame.draw.rect(self.screen, self.color, (item["position"]["x"], item["position"]["y"], self.settings.size_snake, self.settings.size_snake))
            
            self.parts_list[i]["rect"] = rect

            i += 1