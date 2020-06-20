import pygame


class Text:
    def __init__(self, text, x, y, fontSize):
        self.buttonFont = pygame.font.SysFont("Bauhaus93", fontSize)
        self.text = text
        self.y = y
        self.x = x

    def draw(self, screen, colour):
        screen.blit(self.buttonFont.render(self.text, 1, colour), (self.x, self.y))
