import random

from dino_runner.components.obstacles.obstacles import Obstacle


class Bird(Obstacle):
    def __init__(self, image):
        super().__init__(image, 0)
        self.y_position = [270, 220, 320]
        self.rect.y = random.choice(self.y_position)
        self.index = 0

    def draw(self, screen):
        if self.index == 9:
           self.index = 0
        
        screen.blit(self.image[self.index//5], self.rect)
        self.index += 1