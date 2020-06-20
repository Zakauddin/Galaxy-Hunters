import pygame
import colours
import random


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 250, 100)
        self.colour = colours.ORANGE

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect, 1)


class Ship(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.rect = pygame.Rect(random.randint(0, 1199), random.randint(0, 569), 80, 80)
        self.colour = colours.BLUE
        self.dx = speed
        self.dy = random.randint(-5, 5)
        self.ships = [pygame.image.load("images/spaceship1.png"), pygame.image.load("images/spaceship2.png"),
                      pygame.image.load("images/spaceship3.png")]
        self.ship = random.choice(self.ships)
        self.shipScore = 0
        if self.ship == self.ships[0]:
            self.shipScore = 1
        elif self.ship == self.ships[1]:
            self.shipScore = 3
        elif self.ship == self.ships[2]:
            self.shipScore = 5

    def draw(self, screen):
        screen.blit(self.ship, self.rect)

    def update(self):

        self.rect[0] += self.dx
        if self.rect[0] >= 1280 - 80:
            self.dx = - self.dx
        elif self.rect[0] <= 0:
            self.dx = - self.dx

        self.rect[1] += self.dy
        if self.rect[1] <= 0:
            self.dy = - self.dy
        elif self.rect[1] >= 720 - 80 - 70:
            self.dy = - self.dy


class CrossHair(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 20, 20)
        self.image = pygame.image.load("images/crosshair.png")

    def draw(self, screen):
        x, y = pygame.mouse.get_pos()
        self.rect[0] = x - 10
        self.rect[1] = y - 10
        screen.blit(self.image, self.rect)
