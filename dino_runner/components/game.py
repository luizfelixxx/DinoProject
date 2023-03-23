import pygame

from dino_runner.utils.constants import *
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.button import Button # Ideia do Menu_pause
from dino_runner.components.obstacles.obstaclesManager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.components.cloud import Cloud # nuvens


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
        self.game_paused = False # menu_pause
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.score = 0
        self.death_count = 0
        
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
        self.cloud = Cloud()
        # Ideia LeardBoard
        self.leaderboard = []
        
        # Lista de botões 
        self.leaderboard_button = Button(550, 150, BUTTONS[0], 0.8)
        self.resume_button = Button(550, 250, BUTTONS[1], 0.8) 
        self.quit_button = Button(550, 350, BUTTONS[2], 0.8)

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
            if self.game_paused: # menu_pause 
                self.menu_pause()# 
            else:
                self.events()
                self.update()
                self.draw()
        self.score_leaderboard() # Ideia do Leaderboard 
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN: # Ideia Menu
                if event.key == pygame.K_ESCAPE: # 
                    self.game_paused = True # 
            
            if event.type == pygame.QUIT:
                self.playing = False
                self.running= False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self)
        self.cloud.update(self)

    def update_score(self):
        self.score += 1
        if  self.score % 100 == 0:
            self.game_speed += 2
            SCORE_SOUND.play()
    
    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill(COLOR_WHITE)
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.draw_power_up_time()#
        self.draw_speed()#
        self.draw_menu_pause()#
        self.power_up_manager.draw(self.screen)#
        self.cloud.draw(self.screen)
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
    
    # Ideia nenu
    def draw_menu_pause(self):
        self.draw_text("Press Esc to pause", 20, COLOR_BLACK, 120, 580)
    
    # Histórico de pontuação 
    def draw_leaderboard(self):
        with open("leader.txt", "r") as arquivo:
            valores = arquivo.readlines()
            valores = [int(valor) for valor in valores]   
            valores.sort(reverse= True)
        ranking = ""
        for i, valor in enumerate(valores[:5]):
            ranking += f"{i+1}ºplace: {valor} "
        self.draw_text(f"Leaderboard: {ranking} ", 18, COLOR_BLACK, SCREEN_WIDTH - 650, 20)  
    
    def draw_text(self, texto, tamanho, cor,  x, y): 
        font = pygame.font.Font(FONT, tamanho)
        text = font.render(texto, True, cor)
        text_rect = text.get_rect()
        text_rect.center = (x,y)
        self.screen.blit(text, text_rect)
    
    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 1)
            if time_to_show >= 0.1 and self.player.type in [SHIELD_TYPE, HAMMER_TYPE]:
                self.draw_text(f"{self.player.type.capitalize()} enabled for {time_to_show} seconds", 15, COLOR_BLACK, 550, 40) 
            elif time_to_show >= 5 and self.player.type == HEART_TYPE:
                self.draw_text(f"{self.player.type.capitalize()} Your Speed ​​has been changed to 20 ", 15, COLOR_BLACK, 550, 40) 
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE
    
    def draw_speed(self): #
        self.draw_text(f"Game Speed: {self.game_speed}", 20, COLOR_BLACK, 1000, 20)

    def draw_score(self):
        self.draw_text(f"Score: {self.score} ", 20, COLOR_BLACK, 1000, 50)
    
    # Armazenar a pontuação
    def score_leaderboard(self):
        self.leaderboard.append(self.score) #
        with open("leader.txt", "a") as arquivo: #
            for valor in self.leaderboard: #
                arquivo.write(str(valor) + "\n") #
        self.leaderboard = []
       
    
    # Ideia Pausar/Menu/Opções
    def handle_events_menu_pause(self):       
        for event in pygame.event.get(): # 
            if event.type == pygame.QUIT:
                self.game_paused = False
                self.playing = False
                self.running = False

    # Ideia Pausar/Menu/Opções 
    def menu_pause(self):
        while self.game_paused: 
            if self.resume_button.draw(self.screen):
                self.game_paused = False        
            elif self.leaderboard_button.draw(self.screen):
                self.draw_leaderboard()   
            elif self.quit_button.draw(self.screen):
                self.game_paused = False
                self.playing = False     
                self.running = False
            
            pygame.display.flip()

            self.handle_events_menu_pause()
    
    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                   self.run()

    def show_menu(self):
        half_screen_height = SCREEN_HEIGHT//2
        half_screen_width = SCREEN_WIDTH//2

        if self.death_count == 0:
            self.screen.fill(COLOR_BLACK)
            self.draw_text("Press enter to start", 20, COLOR_WHITE, 548, 450)
            self.draw_text("Felix development", 20, COLOR_WHITE, 548, 550)
            self.screen.blit(START_LOGO, (half_screen_width-300, half_screen_height-200))
        else:
            self.screen.fill(COLOR_WHITE)
            self.draw_text("Press enter to restart", 20, COLOR_BLACK, 550, 300)
            self.draw_text(f"Score: {self.score}", 18, COLOR_BLACK, 550, 350)
            self.draw_text(f"Deaths: {self.death_count}", 18, COLOR_BLACK, 550, 400)
            self.screen.blit(ICON, (half_screen_width-42, half_screen_height-140))
            
        pygame.display.update()

        self.handle_events_on_menu()
     
    def reset_game(self):
        self.player.has_power_up = False
        self.obstacle_manager.obstacles = []
        self.score = 0
        self.game_speed = 20