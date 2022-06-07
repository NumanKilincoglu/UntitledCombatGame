import pygame.sprite

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            "/assets/Characters/HeroKnight/Idle/0.png")
        self.image = pygame.transform.scale(self.image,
                                            (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def drawCharacter(self):
        Screen.blit(self.image, self.rect)
