import pygame

class Dance:
    def __init__(self, name: str, angle: int, x: int, y: int) -> None:
        self.imageCreature = pygame.image.load("img/" + name + ".png").convert()
        self.image = self.imageCreature
        self.rect = self.image.get_rect()
        self.angle = angle
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        
        self.speed = 1
        self.turn = True

    def update(self):
        prev_center = self.rect.center
        self.image = pygame.transform.rotate(self.imageCreature, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = prev_center

    def animate(self):
        self.update()
        if self.turn: 
            self.angle -= 45
            self.turn = False
        else: 
            self.angle += 45
            self.turn = True