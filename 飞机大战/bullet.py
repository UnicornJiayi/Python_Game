import pygame

class Bullet1(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/bullet1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = position
        self.speed = 12
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed #炸弹只需要修改top位置

        if self.rect.top < 0:
            self.active = False

    def reset(self,position): #reset相当于再一次初始化
        self.rect.left,self.rect.top = position
        self.active = True

    
        
