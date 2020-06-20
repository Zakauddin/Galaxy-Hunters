import pygame
import states


pygame.init()

WIDTH = 1280
HEIGHT = 720
gameDisplay = pygame.display.set_mode([WIDTH, HEIGHT])

pygame.display.set_caption('Galaxy Hunters')

clock = pygame.time.Clock()

stateManager = states.StateManager()
mainMenu = states.MainMenu(stateManager, gameDisplay)
stateManager.changeState(mainMenu)

while not stateManager.done:
    stateManager.state.handleEvents()
    stateManager.state.update()
    stateManager.state.draw()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
