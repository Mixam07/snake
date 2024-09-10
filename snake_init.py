import sys
from time import sleep

import pygame

from settings import Settings
from scoreboard import Scoreboard
from button import Button
from snake import Snake
from apple import Apple

class SnakeInit:
    """Загальний клас для керування ресурсами та поведінкою гри"""
    def __init__(self):
        """Ініціалізувати гру, створити ресурси гри"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption(self.settings.caption)

        self.snake = Snake(self)
        self.apple = Apple(self)
        self.sb = Scoreboard(self)
        
        #Розпочати гру в не активному стані
        self.game_active = False

        #Створити кнопку Play
        self.play_button = Button(self, "Play")

    def run_game(self):
        while True:
            self._check_events()

            if self.game_active:
                self.snake.update()
                self._check_is_snike_hite()
                self._check_is_snake_ate_apple()
                self._check_is_snake_bumped()
                self.sb.prep_score()

            self._update_screen()

    def _check_events(self):
        """Реагувати на натискання клавіш та події миші"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event): 
        """Реагувати на натискання клавіш"""
        if event.key == pygame.K_RIGHT and not self.snake.moving_direction == "left":
            self.snake.moving_direction = "right"
            self.snake.y = self.snake.parts_list[0]["position"]["y"]
        elif event.key == pygame.K_LEFT and not self.snake.moving_direction == "right":
            self.snake.moving_direction = "left"
            self.snake.y = self.snake.parts_list[0]["position"]["y"]
        elif event.key == pygame.K_UP and not self.snake.moving_direction == "bottom":
            self.snake.moving_direction = "top"
            self.snake.x = self.snake.parts_list[0]["position"]["x"]
        elif event.key == pygame.K_DOWN and not self.snake.moving_direction == "top":
            self.snake.moving_direction = "bottom"
            self.snake.x = self.snake.parts_list[0]["position"]["x"]
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_is_snike_hite(self):
        """Перевірити, чи не досягла змійка якоїсь грані"""
        screen_rect = self.screen.get_rect()
        rect = self.snake.rect

        if(rect["x"] <= screen_rect.left - self.settings.size_snake or
            rect["x"] >= screen_rect.right or
            rect["y"] <= screen_rect.top - self.settings.size_snake or
            rect["y"] >= screen_rect.bottom):
            #Зреагувати так, ніби змійка врізалася
            self._snake_hit()
        

    def _snake_hit(self):
        """Реагувати на зіткнення змійки"""
        #Аналювати налаштування змійки
        self.snake.number_parts = self.settings.start_number_parts
        self.snake.center_snake()
        self.snake.init_snake()
        self.snake.moving_direction = "top"

        #Змінити позицію яблука
        self.apple.generate_position()

        #Відображення кнопки
        self.play_button.visible = True
        self.game_active = False
        pygame.mouse.set_visible(True)

        #Пауза
        sleep(0.5)

        pygame.display.flip()
        
    def _check_is_snake_ate_apple(self):
        """Перевірка чи змікці з'їла яблуко"""
        for item in self.snake.parts_list:
            if item.get("rect"):
                if item["rect"].colliderect(self.apple.rect):
                    self.apple.generate_position()
                    self.snake.number_parts += 1

                    break

    def _check_is_snake_bumped(self):
        """Перевірка чи змікці врізалася в себе"""
        for item in self.snake.parts_list[1:]:
            if item.get("rect") and self.snake.parts_list[0].get("rect"):
                if item["rect"].colliderect(self.snake.parts_list[0]["rect"]):
                    #Зреагувати так, ніби змійка врізалася
                    self._snake_hit()

                    break

    def _check_play_button(self, mouse_pos):
        """Розпочати нову гру, коли користувач натисне кнопку Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.game_active:
            #Сховати кнопку
            self.game_active = True
            self.play_button.visible = False
            pygame.mouse.set_visible(False)

    def _update_screen(self):
        """Оновити зображення на екрані та перемкнутися на новий екран"""
        self.screen.fill(self.settings.bg_color)

        #Відмальовування всіх об'єктів
        self.snake.blitme()
        self.apple.blitme()
        self.sb.show_score()
        self.play_button.draw_button()

        pygame.display.flip()

if __name__ == '__main__':
    #Створити екземпляр гри та запустити гру
    snake = SnakeInit()
    snake.run_game()