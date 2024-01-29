import pygame
import colours
import sprites
import texts
import scorefile


class StateManager:

    def __init__(self):
        super().__init__()
        self.done = False
        self.state = ""

    def changeState(self, state):
        self.state = state


class MainMenu:
    def __init__(self, stateManager, gameDisplay):
        super().__init__()
        self.stateManager = stateManager

        self.backgroundPosition = [0, 0]

        self.gameDisplay = gameDisplay
        self.backgroundImage = pygame.image.load("images/background.jpg")
        self.buttons = [sprites.Button(850, 100), sprites.Button(850, 250),
                        sprites.Button(850, 400), sprites.Button(850, 550)]
        self.labels = [texts.Text("PLAY!", 890, 130, 80), texts.Text("How To Play!", 890, 285, 40),
                       texts.Text("High Scores!", 890, 435, 40), texts.Text("Quit!", 900, 575, 80)]

    def handleEvents(self):

        x, y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stateManager.done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == 1:
                    if self.buttons[0].rect.collidepoint(x, y):
                        self.stateManager.state = Gameplay(self.stateManager, self.gameDisplay)
                    if self.buttons[1].rect.collidepoint(x, y):
                        self.stateManager.state = Instructions(self.stateManager, self.gameDisplay)
                    if self.buttons[2].rect.collidepoint(x, y):
                        self.stateManager.state = HighScores(self.stateManager, self.gameDisplay)
                    if self.buttons[3].rect.collidepoint(x, y):
                        self.stateManager.state = Quit(self.stateManager, self.gameDisplay)

    def draw(self):

        self.gameDisplay.blit(self.backgroundImage, self.backgroundPosition)

        for button in self.buttons:
            button.draw(self.gameDisplay)

        for label in self.labels:
            label.draw(self.gameDisplay, colours.YELLOW)

    def update(self):

        x, y = pygame.mouse.get_pos()

        for button in self.buttons:
            if button.rect.collidepoint(x, y):
                button.colour = colours.BLACK
            else:
                button.colour = colours.ORANGE


class Gameplay:

    def __init__(self, stateManager, gameDisplay):
        super().__init__()
        self.stateManager = stateManager
        self.backgroundPosition = [0, 0]
        self.gameDisplay = gameDisplay
        self.backgroundImage = pygame.image.load("images/gameplayBackground.jpg")
        self.speed = 6
        self.spaceShip = sprites.Ship(self.speed)
        self.totalShips = 0
        self.hud = (0, 650, 1280, 70)
        self.crossHair = sprites.CrossHair()
        self.lives = 3
        self.shotsLeft = 2
        self.score = 0
        self.labels = [texts.Text("Lives:", 130, 670, 40), texts.Text(str(self.lives), 280, 670, 40),
                       texts.Text("Shots left:", 450, 670, 40), texts.Text(str(self.shotsLeft), 650, 670, 40),
                       texts.Text("Score:", 950, 670, 40), texts.Text(str(self.score), 1150, 670, 40)]
        self.gameOver = [texts.Text("GameOver", 400, 300, 100), texts.Text("Press the ESC key to exit.", 10, 10, 40),
                         texts.Text("Press the 'R' key to restart.", 10, 60, 40)]
        self.file = scorefile.HighscoreFile()

    def handleEvents(self):

        x, y = pygame.mouse.get_pos()
        pygame.mouse.set_visible(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stateManager.done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mouse.set_visible(1)
                    self.stateManager.state = MainMenu(self.stateManager, self.gameDisplay)
                    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == 1:
                    if self.spaceShip.rect.collidepoint(x, y):
                        if self.shotsLeft != 0:
                            self.score = self.score + self.spaceShip.shipScore
                            self.labels[5] = texts.Text(str(self.score), 1150, 670, 40)
                            self.shotsLeft = 2
                            self.labels[3] = texts.Text(str(self.shotsLeft), 650, 670, 40)
                            self.totalShips += 1
                            self.spaceShip = ""
                            self.spaceShip = sprites.Ship(self.speed)
                            if self.totalShips % 10 == 0:
                                self.speed += 4

                    else:
                        if self.lives > 0:
                            if self.shotsLeft == 1:
                                self.lives -= 1
                                self.labels[1] = texts.Text(str(self.lives), 280, 670, 40)
                                self.shotsLeft = 2
                                self.labels[3] = texts.Text(str(self.shotsLeft), 650, 670, 40)
                                self.spaceShip = ""
                                self.spaceShip = sprites.Ship(self.speed)

                            elif self.shotsLeft == 2:
                                self.shotsLeft -= 1
                                self.labels[3] = texts.Text(str(self.shotsLeft), 650, 670, 40)

                        if self.lives == 0:
                            self.shotsLeft = 0
                            self.labels[3] = texts.Text(str(self.shotsLeft), 650, 670, 40)
                            pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                            if self.score > self.file.fileInfo[19]:
                                self.stateManager.state = Username(self.stateManager, self.gameDisplay, self.score)
                                pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if self.lives == 0:
                        self.stateManager.state = Gameplay(self.stateManager, self.gameDisplay)
                        pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)

    def draw(self):

        self.gameDisplay.blit(self.backgroundImage, self.backgroundPosition)

        self.spaceShip.draw(self.gameDisplay)

        self.crossHair.draw(self.gameDisplay)

        pygame.draw.rect(self.gameDisplay, colours.BLACK, self.hud)

        for label in self.labels:
            label.draw(self.gameDisplay, colours.YELLOW)

        if self.lives == 0:
            for text in self.gameOver:
                text.draw(self.gameDisplay, colours.YELLOW)

    def update(self):

        self.spaceShip.update()


class Username:

    def __init__(self, stateManager, gameDisplay, score):
        super().__init__()
        self.stateManager = stateManager
        self.backgroundPosition = [0, 0]
        self.gameDisplay = gameDisplay
        self.backgroundImage = pygame.image.load("images/gameplayBackground.jpg")
        self.score = score
        self.labels = [texts.Text("Game Over", 300, 100, 100),
                       texts.Text("New High score", 300, 200, 100),
                       texts.Text("Please enter your name here: ", 300, 400, 45),
                       texts.Text("*Please make sure name is maximum six letters.", 300, 450, 30)]
        self.username = ""
        self.usernameDisplay = texts.Text(self.username, 500, 550, 50)
        self.file = scorefile.HighscoreFile()
        self.warning = texts.Text("Please enter a name with with 6 letters maximum.", 300, 650, 30)
        self.warningTrue = False

    def handleEvents(self):

        pygame.mouse.set_visible(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stateManager.done = True

            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    self.username += event.unicode
                    self.usernameDisplay = texts.Text(self.username, 500, 550, 50)
                elif event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                    self.usernameDisplay = texts.Text(self.username, 500, 550, 50)
                elif event.key == pygame.K_RETURN:
                    if self.username == "" or len(self.username) > 6:
                        self.username = ""
                        self.usernameDisplay = texts.Text(self.username, 500, 600, 50)
                        self.warningTrue = True
                    else:
                        self.file.newScore(self.score, self.username)
                        self.stateManager.state = MainMenu(self.stateManager, self.gameDisplay)

    def draw(self):

        self.gameDisplay.blit(self.backgroundImage, self.backgroundPosition)

        self.usernameDisplay.draw(self.gameDisplay, colours.YELLOW)

        if self.warningTrue:
            self.warning.draw(self.gameDisplay, colours.RED)

        for label in self.labels:
            label.draw(self.gameDisplay, colours.YELLOW)

    def update(self):
        pass


class Instructions:

    def __init__(self, stateManager, gameDisplay):
        super().__init__()
        self.stateManager = stateManager
        self.backgroundPosition = [0, 0]
        self.gameDisplay = gameDisplay
        self.backgroundImage = [pygame.image.load("images/hud.jpg"), pygame.image.load("images/controls.jpg"),
                                pygame.image.load("images/points.jpg"), pygame.image.load("images/info.jpg")]
        self.nextImage = 0
        self.buttons = [sprites.Button(10, 10), sprites.Button(1020, 610)]
        self.buttonText = [texts.Text("Main Menu", 50, 45, 45), texts.Text("Next", 1090, 625, 60)]

    def handleEvents(self):

        x, y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stateManager.done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == 1:
                    if self.buttons[0].rect.collidepoint(x, y):
                        self.stateManager.state = MainMenu(self.stateManager, self.gameDisplay)
                    if self.buttons[1].rect.collidepoint(x, y):
                        if self.nextImage == 3:
                            self.nextImage = 0
                        else:
                            self.nextImage += 1

    def draw(self):

        self.gameDisplay.blit(self.backgroundImage[self.nextImage], self.backgroundPosition)

        for button in self.buttons:
            button.draw(self.gameDisplay)

        for text in self.buttonText:
            text.draw(self.gameDisplay, colours.YELLOW)

    def update(self):

        x, y = pygame.mouse.get_pos()

        for button in self.buttons:
            if button.rect.collidepoint(x, y):
                button.colour = colours.BLACK
            else:
                button.colour = colours.WHITE


class HighScores:

    def __init__(self, stateManager, gameDisplay):
        super().__init__()
        self.stateManager = stateManager
        self.backgroundPosition = [0, 0]
        self.gameDisplay = gameDisplay
        self.backgroundImage = pygame.image.load("images/gameplayBackground.jpg")
        self.backButton = sprites.Button(10, 10)
        self.file = scorefile.HighscoreFile()
        self.labels = [texts.Text("Main Menu", 50, 45, 45), texts.Text("High Scores", 450, 35, 80)]

    def handleEvents(self):

        x, y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stateManager.done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == 1:
                    if self.backButton.rect.collidepoint(x, y):
                        self.stateManager.state = MainMenu(self.stateManager, self.gameDisplay)

    def draw(self):

        self.gameDisplay.blit(self.backgroundImage, self.backgroundPosition)

        self.backButton.draw(self.gameDisplay)

        for text in self.labels:
            text.draw(self.gameDisplay, colours.YELLOW)

        self.file.draw(self.gameDisplay, colours.YELLOW)

    def update(self):

        x, y = pygame.mouse.get_pos()

        if self.backButton.rect.collidepoint(x, y):
            self.backButton.colour = colours.BLACK
        else:
            self.backButton.colour = colours.ORANGE


class Quit:

    def __init__(self, stateManager, gameDisplay):
        super().__init__()
        self.stateManager = stateManager
        self.backgroundPosition = [0, 0]
        self.gameDisplay = gameDisplay
        self.backgroundImage = pygame.image.load("images/quit.jpg")
        self.buttons = [sprites.Button(400, 350), sprites.Button(700, 350)]
        self.labels = [texts.Text("Are you sure?", 200, 100, 150), texts.Text("YES!", 450, 350, 80),
                       texts.Text("NO", 775, 350, 80)]

    def handleEvents(self):

        x, y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stateManager.done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == 1:
                    if self.buttons[0].rect.collidepoint(x, y):
                        self.stateManager.done = True
                    if self.buttons[1].rect.collidepoint(x, y):
                        self.stateManager.state = MainMenu(self.stateManager, self.gameDisplay)

    def draw(self):

        self.gameDisplay.blit(self.backgroundImage, self.backgroundPosition)

        for button in self.buttons:
            button.draw(self.gameDisplay)

        for label in self.labels:
            label.draw(self.gameDisplay, colours.YELLOW)

    def update(self):

        x, y = pygame.mouse.get_pos()

        for button in self.buttons:
            if button.rect.collidepoint(x, y):
                button.colour = colours.BLACK
            else:
                button.colour = colours.ORANGE
