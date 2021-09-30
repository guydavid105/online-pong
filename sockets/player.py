import pygame


class Player:
    def __init__(self, x, y, width1, height1, colour, players):
        self.x = x
        self.y = y
        self.width = width1
        self.height = height1
        self.colour = colour
        self.rect = (x, y, width1, height1)
        self.vel = 7
        self.players = players

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.y > 25:
            self.y -= self.vel
        if keys[pygame.K_DOWN] and self.y < (475 - self.height):
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
