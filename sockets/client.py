import pygame
from network import Network
from player import Player
import time

pygame.init()

width = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

client_number = 0
score1 = 0
score2 = 0
font = pygame.font.SysFont("Bauhaus 93", 30)
blue = (0, 0, 255)
wait = False


def draw_text(text, font1, text_col, x, y):
    img = font1.render(text, True, text_col)
    screen.blit(img, (x, y))


class Ball:
    def __init__(self, x, y):
        ball_img = pygame.image.load("pong ball.png")
        self.image = pygame.transform.scale(ball_img, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dir_x = 1
        self.dir_y = 1
        self.l1 = False
        self.l2 = False
        self.vel = 5

    def move(self):
        if self.rect.y <= 0 or self.rect.y >= 500:
            self.dir_y *= -1
        if self.l1:
            self.dir_x *= -1
            self.l1 = False
            if self.dir_y == 0:
                self.dir_y = -1
        if self.l2:
            self.dir_x *= -1
            self.l2 = False
            if self.dir_y == 0:
                self.dir_y = 1
        self.rect.x += (self.vel * self.dir_x)
        self.rect.y += (self.vel * self.dir_y)

    def edges(self):
        if self.rect.x <= 0 or self.rect.x >= 500:
            return True

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.move()
        self.edges()


def redraw_window(win, players, players2, ball):
    screen.fill((0, 0, 0))
    players.draw(screen)
    players2.draw(screen)
    ball.draw()
    pygame.draw.line(screen, (255, 255, 255), (250, 500), (250, 0), 5)
    draw_text(str(score1), font, blue, 100, 100)
    draw_text(str(score2), font, blue, 400, 100)
    pygame.display.update()


run = True
n = Network()
player = n.getP()
ball = Ball(250, 250)
clock = pygame.time.Clock()

while run:
    clock.tick(60)
    player2 = n.send(player)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
    if player.players == 2 or player2.players == 2:
        player.move()
        ball.update()
        if ball.rect.colliderect(player.rect) or ball.rect.colliderect(player2.rect):
            ball.dir_x *= -1
            if ball.dir_y == 0:
                ball.dir_y = 1
        if ball.edges():
            if ball.rect.x + 10 <= 0:
                score2 += 1
                ball.rect.x = 250
                ball.rect.y = 250
                ball.dir_y = 0
                wait = True
            if ball.rect.x >= 500:
                score1 += 1
                ball.rect.x = 250
                ball.rect.y = 250
                ball.dir_y = 0
                wait = True
        if score2 == 5:
            screen.fill((0, 0, 0))
            draw_text("Right side player has won!", font, blue, 50, 100)
            pygame.display.update()
            time.sleep(4)
            run = False
        if score1 == 5:
            screen.fill((0, 0, 0))
            draw_text("Left side player has won!", font, blue, 50, 100)
            pygame.display.update()
            time.sleep(4)
            run = False
        redraw_window(screen, player, player2, ball)
        if wait:
            time.sleep(1)
            wait = False
