import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT, COLOR_BLACK, COLOR_WHITE, DEFAULT_TYPE
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstaclesManager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.score = 0
        self.death_count = 0
        
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        self.playing = True
        self.reset_game()
        self.power_up_manager.reset_power_ups()
        while self.playing:
            self.events()
            self.update()
            self.draw()
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self.score, self.game_speed, self.player)

    def update_score(self):
        self.score += 1
        if  self.score % 100 == 0:
            self.game_speed += 5
    
    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill(COLOR_WHITE)
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.draw_power_up_time()#
        self.power_up_manager.draw(self.screen)#
        pygame.display.update()
        pygame.display.flip()
 
    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
    
    def draw_text(self, texto, tamanho, cor,  x, y): # Add 20/03
        font = pygame.font.Font(FONT, tamanho)
        text = font.render(texto, True, cor)
        text_rect = text.get_rect()
        text_rect.center = (x,y)
        self.screen.blit(text, text_rect)
    
    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                self.draw_text(f"{self.player.type.capitalize()} enabled for{time_to_show} seconds", 15, COLOR_BLACK, 500, 40) 
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def draw_score(self):
        self.draw_text(f"Score: {self.score} ", 20, COLOR_BLACK, 1000, 50)
    
    def reset_game(self):
        self.obstacle_manager.reset_obstacles()
        self.score = 0
        self.game_speed = 20
    
    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def show_menu(self):
        self.screen.fill(COLOR_WHITE)
        half_screen_height = SCREEN_HEIGHT//2
        half_screen_width = SCREEN_WIDTH//2

        if self.death_count == 0:
            self.draw_text("Press any key to start", 22, COLOR_BLACK, 548, 250)
        else:
            self.draw_text("Press any key to restart", 20, COLOR_BLACK, 550, 300)
            self.draw_text(f"Score: {self.score}", 18, COLOR_BLACK, 550, 350)
            self.draw_text(f"Deaths: {self.death_count}", 18, COLOR_BLACK, 550, 400)
            self.screen.blit(ICON, (half_screen_width-45, half_screen_height-140))
            
        pygame.display.update()

        self.handle_events_on_menu()