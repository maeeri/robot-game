import pygame
from random import randint
from GameObject import Monster, Coin, Robot
from Dance import Dance

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen_height = 600
        self.screen_width = 900
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.clock = pygame.time.Clock()

        self.monsters = [
            Monster(self.screen_width, self.screen_height, False, True, False)
        ]

        self.coins = [
            Coin(self.screen_width, self.screen_height),
        ]

        self.points = 0
        self.lives = 3

        self.game_over = False
        self.victory = False
        self.start = True

        self.robot = Robot(self.screen_width, self.screen_height)
        self.dance = Dance("robo", 22, self.screen_width/2 - 20, 350)

        pygame.display.set_caption("Oil change")
        self.loop()

    def draw_display(self):
        if self.start:
            self.start_screen()
        elif self.game_over:
            self.game_over_screen()
        elif self.victory:
            self.win_screen()
        else:
            self.game_screen()
    
    def read_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            self.robot.robot_movement(event)
            if event.type == pygame.KEYDOWN:
                if (self.game_over or self.victory) and (event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN):
                    self.new_game()
                if self.start and (event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN):
                    self.start = False

    def objects_move(self):
        for monster in self.monsters:
            monster.move_monster(self.robot)  
        self.robot.move_robot()

    def loop(self):
        while True:
            self.read_events()
            self.objects_move()
            self.draw_display()
            

    def collect_coin(self):
        coin_sound = pygame.mixer.Sound("sound/coin.mp3")
        victory_sound = pygame.mixer.Sound("sound/victory.wav")
        for k in self.coins:
            condition_x = abs(k.center_x - self.robot.center_x) <= (k.width + self.robot.width)/2
            condition_y = abs(k.center_y - self.robot.center_y) <= (k.height + self.robot.height)/2
            if condition_x and condition_y:
                k.random_coin_placement()
                pygame.mixer.Sound.play(coin_sound)
                self.points += 1
            if self.points >= 20:
                pygame.mixer.Sound.play(victory_sound)
                self.victory = True

    def encounter_monster(self):
        monster_sound = pygame.mixer.Sound("sound/life_lost.wav")
        game_over_sound = pygame.mixer.Sound("sound/game_over.wav")
        for h in self.monsters:
            condition_x = abs(h.center_x - self.robot.center_x) <= (h.width + self.robot.width)/2
            condition_y = abs(h.center_y - self.robot.center_y) <= (h.height + self.robot.height)/2
            if condition_x and condition_y:
                pygame.mixer.Sound.play(monster_sound)
                h.new_spot()
                self.lives -= 1
            if self.lives < 1:
                pygame.mixer.Sound.play(game_over_sound)
                self.game_over = True

    def control_monsters(self):
        if len(self.monsters) == 3 and self.points >= 10:
            self.monsters.append(Monster(self.screen_width, self.screen_height, False, True, False))
        if len(self.monsters) == 1 and self.points >= 4 or len(self.monsters) == 4 and self.points >= 12:
            self.monsters.append(Monster(self.screen_width, self.screen_height, False, False, True))
        if len(self.monsters) == 2 and self.points >= 7 or len(self.monsters) == 5 and self.points>= 14:
            self.monsters.append(Monster(self.screen_width, self.screen_height, False, True, True))
        if len(self.monsters) == 6 and self.points >= 17:
            self.monsters.append(Monster(self.screen_width, self.screen_height, True, False, False))
        if len(self.monsters) == 6 and len(self.coins) == 1:
            self.coins.append(Coin(self.screen_width, self.screen_height))
    
    def game_over_screen(self):
        self.screen.fill((0,0,0))
        self.points_display()
        title_font = pygame.font.SysFont("Arial", 50)
        body_font = pygame.font.SysFont("Arial", 20)
        title = title_font.render("GAME OVER :'(", True, ((255, 0, 0)))
        line = body_font.render("Return to start screen by pressing 'Enter'", True, ((255,255,255)))
        self.screen.blit(title, ((self.screen_width - title.get_width())/2, (self.screen_height - title.get_height())/2 - 20))
        self.screen.blit(line, ((self.screen_width - line.get_width())/2, (self.screen_height - title.get_height())/2  + 40))

        pygame.display.flip()

    def game_screen(self):
        self.screen.fill((200,200,200))

        self.points_display()
        self.control_monsters()
        for coin in self.coins:
            self.screen.blit(coin.image, (coin.x, coin.y))

        self.screen.blit(self.robot.image, (self.robot.x, self.robot.y))

        for monster in self.monsters:
            self.screen.blit(monster.image, (monster.x, monster.y))

        self.collect_coin()
        self.encounter_monster()

        pygame.display.flip()
        self.clock.tick(60)

    def win_screen(self):
        self.screen.fill((0,0,0))
        self.points_display()
        title_font = pygame.font.SysFont("Arial", 50)
        body_font = pygame.font.SysFont("Arial", 20)
        title = title_font.render("YOU WON!!!", True, ((255, 0, 0)))
        self.screen.blit(title, ((self.screen_width - title.get_width())/2, (self.screen_height - title.get_height())/2-40))

        line = body_font.render("Return to start screen by pressing 'Enter'", True, ((255,255,255)))
        self.screen.blit(line, ((self.screen_width - line.get_width())/2, (self.screen_height - title.get_height())/2 + 40))

        self.screen.blit(self.dance.image, (self.dance.x, self.dance.y))
        self.dance.animate()
        
        self.clock.tick(2)
        pygame.display.flip()

    def start_screen(self):
        self.screen.fill((0,0,0))
        title_font = pygame.font.SysFont("Arial", 50)
        body_font = pygame.font.SysFont("Arial", 20)

        contents = [
            "Robodude needs an oil change, but is low on cash :(",
            "Your task is to help Robodude collect 20 coins while avoiding oil monsters",
            "Move Robodude with your arrow keys",
            "Start the game by pressing 'Enter'"
        ]

        for i in range(len(contents)):
            line = body_font.render(contents[i], True, ((255,255,255)))
            self.screen.blit(line, ((self.screen_width - line.get_width())/2, 230 + i * 25))

        robo = pygame.image.load("img/robo.png")
        self.screen.blit(robo, ((self.screen_width - robo.get_width())/2, 340))

        title = title_font.render("Oil change", True, ((255, 0, 0)))
        self.screen.blit(title, ((self.screen_width - title.get_width())/2, 150))

        pygame.display.flip()

    def new_game(self):
        self.__init__()

    def points_display(self):
        pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(self.screen_width - 140, 10, 130, 70))
        font = pygame.font.SysFont("Arial", 24)
        point_text = font.render(f"Coins: {self.points}/20", True, (255, 0, 0))
        life_text = font.render(f"Lives: {self.lives}", True, (255, 0, 0))
        self.screen.blit(point_text, (self.screen_width - 130, 15))
        self.screen.blit(life_text, (self.screen_width - 130, 40))