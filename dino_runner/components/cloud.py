import pygame
import random 
from dino_runner.utils.constants import SCREEN_WIDTH, CLOUD

class Cloud():
    def __init__(self):
        self.position_x = SCREEN_WIDTH + random.randint(200, 3000)
        self.position_y = random.randint(50, 150)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self, game):
        self.position_x -= game.game_speed
        if self.position_x < -self.width:
            self.position_x = SCREEN_WIDTH + random.randint(200, 3000)
            self.position_y = random.randint(50, 150)

    def draw(self, screen):
        screen.blit(self.image, (self.position_x, self.position_y))
