import pygame
import random #

from dino_runner.utils.constants import  SMALL_CACTUS, LARGE_CACTUS, BIRD #
from dino_runner.components.obstacles.cactus import Cactus, CactusLarge #
from dino_runner.components.obstacles.bird import Bird #
from dino_runner.utils.constants import HAMMER_TYPE, SHIELD_TYPE


class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        if len(self.obstacles) == 0:
            dic_obstacle = {0: Cactus(SMALL_CACTUS), 1: CactusLarge(LARGE_CACTUS), 2: Bird(BIRD)}
            rand_num = random.randint(0, 2)
            self.obstacles.append(dic_obstacle[rand_num])
        
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.has_power_up or game.player.slow:
                    pygame.time.delay(500)
                    game.playing = False
                    game.death_count += 1
                    break
                elif game.player.has_power_up and game.player.type == SHIELD_TYPE: 
                    pass
                elif game.player.has_power_up and game.player.type == HAMMER_TYPE: 
                    self.obstacles.remove(obstacle)

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
    
    def reset_obstacles(self):
        self.obstacles = []##
