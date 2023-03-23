import random
import pygame

from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.hammer import Hammer
from dino_runner.components.power_ups.heart import Heart  #
from dino_runner.utils.constants import HAMMER_TYPE, SHIELD_TYPE, HEART_TYPE #


class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.when_appears = 0

    def generate_power_up(self, score):
        list_power_ups = [Hammer(), Shield(), Heart()] #
        if len(self.power_ups) == 0 and self.when_appears == score:
            self.when_appears += random.randint(200, 300)
            power_up = random.choice(list_power_ups)
            self.power_ups.append(power_up)

    def update(self, game):
        self.generate_power_up(game.score)
        for power_up in self.power_ups:
            power_up.update(game.game_speed, self.power_ups)
            if game.player.dino_rect.colliderect(power_up.rect):
                power_up.start_time = pygame.time.get_ticks()
                self.handle_power_up_collision(power_up, game, game.player)
    
    def handle_power_up_collision(self, power_up, game, player): # define the method within the class
        power_up.start_time = pygame.time.get_ticks()
        if power_up.type == HAMMER_TYPE:
            player.hammer = True
            player.shield = False
            player.slow = False
        elif power_up.type == SHIELD_TYPE:
            player.shield = True
            player.hammer = False
            player.slow = False
        elif power_up.type == HEART_TYPE:
            game.game_speed = 20
            player.slow = True 
            player.hammer = False
            player.shield = False
        
        player.has_power_up = True
        player.type = power_up.type
        player.power_up_time = power_up.start_time + (power_up.duration * 1000)
        self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_ups(self):
        self.power_ups = []
        self.when_appears = random.randint(200, 300)

    