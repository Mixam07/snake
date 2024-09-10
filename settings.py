class Settings:
    """Клас для збереження всіх налаштувань гри"""
    def __init__(self):
        """Ініціалізувати постійні налаштування гри"""
        #Налаштування екрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (30, 30, 30)
        self.caption = "Snake"

        #Налаштування змійки
        self.start_number_parts = 3
        self.size_snake = 50
        self.snake_speed = 1.0