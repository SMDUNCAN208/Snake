# Requirements :
# Snake only grows
# Moves faster and grows
# Two players
# Optional : Items that stop the snake and/or shrink it
import pygame, random, sys, time
from pygame.locals import *
from pygame.sprite import *

pygame.init()
snakes = 2
FPS = 15
board = []
windowX = 1000
windowY = 800
smaller = 800
SCREEN = pygame.display.set_mode((windowX, windowY), pygame.RESIZABLE)

pygame.display.set_caption("Snake")
audioFive = pygame.mixer_music.load('musicThingy.mp3')

# Colours
paleBlue   = (215, 228, 255)
darkBlue   = (148, 174, 230)
paleOrange = (255, 235, 214)
darkOrange = (230, 190, 147)
green      = (157, 189, 155)
snakeBlue  = (128, 185, 194)
red        = (200,   0,   0)
black      = (  0,   0,   0)
white      = (255, 255, 255)
darkWhite  = (230, 228, 216)


class boardPiece():
    #number is the snake's order, snakeNum is the player number
    global itemThere, snakeThere, number, snakeNum, lastSnake

    def __init__(self):
        self.itemThere = False
        self.snakeThere = False
        self.number = 0
        self.snakeNum = 0
        self.lastSnake = False

    def getItem(self):
        return self.itemThere

    def changeItem(self, changer):
        self.itemThere = changer

    def getLastSnake(self):
        return self.lastSnake

    def changeLastSnake(self, changer):
        self.lastSnake = changer

    def changeSnakeNum(self, num):
        self.snakeNum = num

    def getSnakeNum(self):
        return self.snakeNum

    def changeNum(self, num):
        self.number = num

    def getNum(self):
        return self.number

    def getSnake(self):
        return self.snakeThere

    def changeSnake(self):
        self.snakeThere = True

    def removeSnake(self):
        self.snakeThere = False
        self.number = 0
        self.snakeNum = 0
        self.lastSnake = False

def main():
    global SCREEN, windowX, windowY, smaller, direction, started, gameOver, twoPlayers, gotItem, scoreOne, scoreTwo, faster, twoLoses, directionTwo

    direction = 1
    directionTwo = 1
    scoreOne = 0
    scoreTwo = 0
    twoPlayers = False
    gotItem = False
    faster = False
    twoLoses = False

    # Change to false to display a starting screen
    started = False
    gameOver = False
    if not twoPlayers :
        createBoard()
    else:
        createBoardTwo()

    drawScreen()
    drawSnake()
    pygame.mixer_music.play(-1, 0.0)

    while True:
        #Normal
        if not gameOver and not twoPlayers and started and not faster:
            if gotItem:
                setItem()
                gotItem = False
            for event in pygame.event.get():
                # Checks key movement

                if event.type == KEYUP and event.key == pygame.K_UP and direction != 2:
                    direction = 1
                if event.type == KEYUP and event.key == pygame.K_DOWN and direction != 1:
                    direction = 2
                if event.type == KEYUP and event.key == pygame.K_RIGHT and direction != 4:
                    direction = 3
                if event.type == KEYUP and event.key == pygame.K_LEFT and direction != 3:
                    direction = 4

                # Screen resizing
                if event.type == pygame.VIDEORESIZE:
                    windowX, windowY = event.w, event.h
                    SCREEN = pygame.display.set_mode((windowX, windowY), pygame.RESIZABLE)
                    if windowX - (windowX / 30) > windowY - (windowY / 30):
                        smaller = windowY
                    else:
                        smaller = windowX
                    drawScreen()


                if event.type == MOUSEBUTTONUP:
                    mouseX, mouseY = event.pos
                    checkButtons(mouseX, mouseY)

                # Quit game
                if event.type == QUIT or (event.type == KEYUP and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            time.sleep(0.1)
            moveSnakePos(gotItem)
            if not gameOver:
                drawSnake()
            else:
                drawScreen()

        #faster
        elif not gameOver and faster and started:
            if gotItem:
                setItem()
                gotItem = False
            for event in pygame.event.get():
                # Checks key movement

                if event.type == KEYUP and event.key == pygame.K_UP and direction != 2:
                    direction = 1
                if event.type == KEYUP and event.key == pygame.K_DOWN and direction != 1:
                    direction = 2
                if event.type == KEYUP and event.key == pygame.K_RIGHT and direction != 4:
                    direction = 3
                if event.type == KEYUP and event.key == pygame.K_LEFT and direction != 3:
                    direction = 4

                # Screen resizing
                if event.type == pygame.VIDEORESIZE:
                    windowX, windowY = event.w, event.h
                    SCREEN = pygame.display.set_mode((windowX, windowY), pygame.RESIZABLE)
                    if windowX - (windowX / 30) > windowY - (windowY / 30):
                        smaller = windowY
                    else:
                        smaller = windowX
                    drawScreen()


                if event.type == MOUSEBUTTONUP:
                    mouseX, mouseY = event.pos
                    checkButtons(mouseX, mouseY)

                # Quit game
                if event.type == QUIT or (event.type == KEYUP and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            if scoreOne < 10:
                time.sleep(0.2 - (0.02 * scoreOne))
            moveSnakePos(gotItem)
            if not gameOver:
                drawSnake()
            else:
                drawScreen()

        #Two Players
        elif not gameOver and twoPlayers and started:
            if gotItem:
                setItem()
                gotItem = False
            for event in pygame.event.get():
                # Checks key movement
                if event.type == KEYUP and event.key == pygame.K_UP and direction != 2:
                    direction = 1
                if event.type == KEYUP and event.key == pygame.K_DOWN and direction != 1:
                    direction = 2
                if event.type == KEYUP and event.key == pygame.K_RIGHT and direction != 4:
                    direction = 3
                if event.type == KEYUP and event.key == pygame.K_LEFT and direction != 3:
                    direction = 4
                #Second Player movement
                if event.type == KEYUP and event.key == pygame.K_w and directionTwo != 2:
                    directionTwo = 1
                if event.type == KEYUP and event.key == pygame.K_s and directionTwo != 1:
                    directionTwo = 2
                if event.type == KEYUP and event.key == pygame.K_d and directionTwo != 4:
                    directionTwo = 3
                if event.type == KEYUP and event.key == pygame.K_a and directionTwo != 3:
                    directionTwo = 4


                # Screen resizing
                if event.type == pygame.VIDEORESIZE:
                    windowX, windowY = event.w, event.h
                    SCREEN = pygame.display.set_mode((windowX, windowY), pygame.RESIZABLE)
                    if windowX - (windowX / 30) > windowY - (windowY / 30):
                        smaller = windowY
                    else:
                        smaller = windowX
                    drawScreen()

                # Mouse motion
                if event.type == MOUSEBUTTONUP:
                    mouseX, mouseY = event.pos
                    checkButtons(mouseX, mouseY)

                # Quit game
                if event.type == QUIT or (event.type == KEYUP and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            time.sleep(0.2)
            moveSnakePos(gotItem)
            if not gameOver:
                drawSnake()
            else:
                drawScreen()

        elif not started or gameOver:
            for event in pygame.event.get():
                #Mouse motion
                if event.type == MOUSEMOTION :
                    mouseX, mouseY = event.pos
                    if mouseX >= ((smaller * 59) / 60) and mouseX <= ((smaller * 59) / 60 + smaller / 4) and mouseY >= (windowY / 3) and mouseY <= ((windowY / 3) + (smaller / 10)):
                        drawButtons(1, darkWhite)
                        pygame.display.update()
                    elif mouseX >= ((smaller * 59) / 60) and mouseX <= ((smaller * 59) / 60 + smaller / 4) and mouseY >= (windowY / 2) and mouseY <= ((windowY / 2) + (smaller / 10)):
                        drawButtons(2, darkWhite)
                        pygame.display.update()
                    elif mouseX >= ((smaller * 59) / 60) and mouseX <= ((smaller * 59) / 60 + smaller / 4) and mouseY >= ((windowY*4)/ 6) and mouseY <= (((windowY*4)/ 6) + (smaller / 10)):
                        drawButtons(3, darkWhite)
                        pygame.display.update()
                    else:
                        drawButtons(1, white)
                        drawButtons(2, white)
                        drawButtons(3, white)

                if event.type == MOUSEBUTTONUP:
                    mouseX, mouseY = event.pos
                    checkButtons(mouseX, mouseY)


                # Screen resizing
                if event.type == pygame.VIDEORESIZE:
                    windowX, windowY = event.w, event.h
                    SCREEN = pygame.display.set_mode((windowX, windowY), pygame.RESIZABLE)
                    if windowX - (windowX / 30) > windowY - (windowY / 30):
                        smaller = windowY
                    else:
                        smaller = windowX
                    drawScreen()

                # Quit game
                if event.type == QUIT or (event.type == KEYUP and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

        else:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                # Screen resizing
                if event.type == pygame.VIDEORESIZE:
                    windowX, windowY = event.w, event.h
                    SCREEN = pygame.display.set_mode((windowX, windowY), pygame.RESIZABLE)
                    if windowX - (windowX / 30) > windowY - (windowY / 30):
                        smaller = windowY
                    else:
                        smaller = windowX
                    drawScreen()

def checkButtons(mouseX, mouseY):
    global started, faster, gameOver, scoreOne, scoreTwo, twoPlayers, direction, directionTwo
    if mouseX >= ((smaller * 59) / 60) and mouseX <= ((smaller * 59) / 60 + smaller / 4) and mouseY >= (windowY / 3) and mouseY <= ((windowY / 3) + (smaller / 10)):
        countDown()
        started = True
        faster = False
        gameOver = False
        twoPlayers = False
        scoreOne, scoreTwo = 0, 0
        createBoard()
        pygame.display.update()
    elif mouseX >= ((smaller * 59) / 60) and mouseX <= ((smaller * 59) / 60 + smaller / 4) and mouseY >= (windowY / 2) and mouseY <= ((windowY / 2) + (smaller / 10)):
        countDown()
        started = True
        faster = True
        gameOver = False
        twoPlayers = False
        scoreOne, scoreTwo = 0, 0
        createBoard()
        pygame.display.update()
    elif mouseX >= ((smaller * 59) / 60) and mouseX <= ((smaller * 59) / 60 + smaller / 4) and mouseY >= ((windowY * 4) / 6) and mouseY <= (((windowY * 4) / 6) + (smaller / 10)):
        countDown()
        started = True
        twoPlayers = True
        faster = False
        gameOver = False
        twoLoses = False
        direction = 1
        directionTwo = 2
        scoreOne, scoreTwo = 0, 0
        createBoardTwo()
        drawScreen()
        pygame.display.update()

def countDown():
    drawGrid()

    dimension = (smaller / 30) * 28
    screenTwo = pygame.Surface((dimension, dimension))
    screenTwo.set_alpha(150)
    screenTwo.fill((0, 0, 0))

    SCREEN.blit(screenTwo, ((smaller / 30), (smaller / 30)))

    fontObj = pygame.font.Font('snakeFont.ttf', int(smaller / 20))
    for i in range(3, 0, -1):
        pygame.draw.rect(SCREEN, paleBlue, ((dimension / 2) + (smaller / 30) - (dimension / 16), (smaller / 30) + (dimension / 2) - (dimension / 16), dimension / 8, dimension / 8))
        textThingy = fontObj.render(str(i), True, darkBlue, None)
        centreX = textThingy.get_width()
        SCREEN.blit(textThingy, ((dimension / 2) + (smaller / 30) - (centreX / 2), dimension / 2))
        pygame.display.update()
        time.sleep(1)

def drawItem():
    for i in range(0, 16, 1):
        for j in range(0, 16, 1):
            if board[i][j].getItem():
                xInt = int((smaller / 30) + ((smaller * i * (28 / 8)) / 60))
                yInt = int((smaller / 30) + ((smaller * j * (28 / 8)) / 60))

                fruitSize = int((((smaller * (1 + i) * (28 / 8)) / 60) - ((smaller * i * (28 / 8)) / 60)) / 2) * 2

                fruit = pygame.image.load("apple.png")
                fruit = pygame.transform.scale(fruit, (fruitSize, fruitSize)).convert_alpha()
                SCREEN.blit(fruit, (xInt, yInt))

def setItem():
    randX = random.randint(0,15)
    randY = random.randint(0,15)
    onSnake = True

    while onSnake:
        randX = random.randint(0, 15)
        randY = random.randint(0, 15)
        if not board[randX][randY].getSnake():
            onSnake = False

    board[randX][randY].changeItem(True)

def drawScreen():
    SCREEN.fill(paleBlue)
    drawGrid()

    fontObj = pygame.font.Font('snakeFont.ttf', int(smaller / 13))
    nameText = fontObj.render("Snake", True, darkBlue, None)
    SCREEN.blit(nameText, ((smaller * 29)/30, windowY/60))

    onePerson = "Score: "
    if twoPlayers:
        onePerson = "Player One: "

    fontObj = pygame.font.Font('snakeFont.ttf', int(smaller / 28))
    if twoPlayers:
        textThingy = fontObj.render(onePerson, True, green, None)
    else:
        textThingy = fontObj.render(onePerson, True, darkBlue, None)
    centreX = textThingy.get_width()
    SCREEN.blit(textThingy, ((smaller * 29)/30, windowY / 6))

    if twoPlayers:
        textThingy = fontObj.render("Player Two: ", True, snakeBlue, None)
        SCREEN.blit(textThingy, ((smaller * 29) / 30, (windowY / 6) + (int(smaller/28))))


    drawButtons(1, white)
    drawButtons(2, white)
    drawButtons(3, white)

    drawItem()
    if gameOver or not started:
        notPlaying()

    pygame.display.update()

def notPlaying():
    dimension = (smaller / 30) * 28
    screenTwo = pygame.Surface((dimension, dimension))
    screenTwo.set_alpha(150)
    screenTwo.fill((0, 0, 0))

    SCREEN.blit(screenTwo, ((smaller / 30) , (smaller / 30)))

    fontObj = pygame.font.Font('snakeFont.ttf', int(smaller / 20))
    if not started:
        textThingy = fontObj.render("Choose a mode to start", True, darkBlue, None)
        centreX = textThingy.get_width()
        SCREEN.blit(textThingy, ((dimension/2) + (smaller/30) - (centreX/2), dimension/2))

    if gameOver and not twoPlayers:
        textThingy = fontObj.render("You lost. Try again.", True, darkBlue, None)
        centreX = textThingy.get_width()
        SCREEN.blit(textThingy, ((dimension / 2) + (smaller / 30) - (centreX / 2), dimension / 2))

    if gameOver and twoPlayers:
        textThingy = fontObj.render("Game over. Try again.", True, darkBlue, None)
        centreX = textThingy.get_width()
        SCREEN.blit(textThingy, ((dimension / 2) + (smaller / 30) - (centreX / 2), dimension / 2))

def drawGrid():
    pygame.draw.rect(SCREEN, paleOrange, (smaller / 30, smaller / 30, (smaller / 30) * 28, (smaller / 30) * 28))
    for i in range(0, 8, 1):
        for j in range(0, 8, 1):
            pygame.draw.rect(SCREEN, darkOrange, (
                (smaller / 30) + ((smaller * i * (28 / 8)) / 30), (smaller / 30) + ((smaller * j * (28 / 8)) / 30),
                (smaller * 28) / 480, (smaller * 28) / 480))

    for i in range(0, 8, 1):
        for j in range(0, 8, 1):
            pygame.draw.rect(SCREEN, darkOrange, (
                (smaller / 30) + ((smaller * i * (28 / 8)) / 30) + ((smaller * (28 / 8)) / 60),
                (smaller / 30) + ((smaller * j * (28 / 8)) / 30) + ((smaller * (28 / 8)) / 60), (smaller * 28) / 480,
                (smaller * 28) / 480))

def drawScores():
    fontObj = pygame.font.Font('snakeFont.ttf', int(smaller / 28))
    onePerson = "Score: "
    if twoPlayers :
        onePerson = "Player Two: "

    textThingy = fontObj.render(onePerson, True, darkBlue, None)
    centreX = textThingy.get_width()

    pygame.draw.rect(SCREEN, paleBlue, (((smaller * 29) / 30) + centreX, windowY / 6, 500, int(smaller/25)))

    if twoPlayers:
        textThingy = fontObj.render(str(scoreOne), True, green, None)
    else:
        textThingy = fontObj.render(str(scoreOne), True, darkBlue, None)
    SCREEN.blit(textThingy, (((smaller * 29) / 30) + centreX, windowY / 6))

    if twoPlayers:
        pygame.draw.rect(SCREEN, paleBlue, (((smaller * 29) / 30) + centreX, (windowY / 6) + (int(smaller / 25)), 500, int(smaller / 25)))
        textThingy = fontObj.render(str(scoreTwo), True, snakeBlue, None)
        SCREEN.blit(textThingy, (((smaller * 29) / 30) + centreX, (windowY / 6) + (int(smaller / 25))))

def drawButtons(button, colourUsed):
    if button == 1:
        # Normal
        pygame.draw.rect(SCREEN, black, ((smaller * 59) / 60, windowY / 3, smaller / 4, smaller / 10))
        pygame.draw.rect(SCREEN, colourUsed, (((smaller * 59) / 60) + 1, (windowY / 3) + 1, (smaller / 4) - 2, (smaller / 10) - 2))
        fontObj = pygame.font.Font('snakeFont.ttf', int(smaller / 28))
        textThingy = fontObj.render("Normal", True, darkBlue, None)
        centreX = textThingy.get_width()
        SCREEN.blit(textThingy, ((((smaller / 4) - 2) / 2) + ((smaller * 59) / 60) - (centreX / 2), (((smaller / 10) - 2) / 2) + ((windowY / 3) + 1) - (smaller / 35)))

    if button == 2:
        # Faster
        pygame.draw.rect(SCREEN, black, ((smaller * 59) / 60, (windowY) / 2, smaller / 4, smaller / 10))
        pygame.draw.rect(SCREEN, colourUsed, (((smaller * 59) / 60) + 1, (windowY / 2) + 1, (smaller / 4) - 2, (smaller / 10) - 2))
        fontObj = pygame.font.Font('snakeFont.ttf', int(smaller / 28))
        textThingy = fontObj.render("Faster", True, darkBlue, None)
        centreX = textThingy.get_width()
        SCREEN.blit(textThingy, ((((smaller / 4) - 2) / 2) + ((smaller * 59) / 60) - (centreX / 2), (((smaller / 10) - 2) / 2) + ((windowY / 2) + 1) - (smaller / 35)))

    if button == 3:
        # Two-Player
        pygame.draw.rect(SCREEN, black, ((smaller * 59) / 60, (windowY * 4) / 6, smaller / 4, smaller / 10))
        pygame.draw.rect(SCREEN, colourUsed, (((smaller * 59) / 60) + 1, ((windowY * 4) / 6) + 1, (smaller / 4) - 2, (smaller / 10) - 2))
        fontObj = pygame.font.Font('snakeFont.ttf', int(smaller / 28))
        textThingy = fontObj.render("Two-Player", True, darkBlue, None)
        centreX = textThingy.get_width()
        SCREEN.blit(textThingy, ((((smaller / 4) - 2) / 2) + ((smaller * 59) / 60) - (centreX / 2), (((smaller / 10) - 2) / 2) + (((windowY * 4) / 6) + 1) - (smaller / 35)))

    pygame.display.update()

def createBoard():
    global board, direction
    board.clear()
    for i in range(0, 16, 1):
        board.append([])

    for i in range(0, 16, 1):
        for j in range(0, 16, 1):
            board[i].append(boardPiece())



    board[7][7].changeSnake()
    board[7][7].changeNum(3)
    board[7][7].changeSnakeNum(1)
    board[7][6].changeSnake()
    board[7][6].changeNum(2)
    board[7][6].changeSnakeNum(1)
    board[7][5].changeSnake()
    board[7][5].changeNum(1)
    board[7][5].changeSnakeNum(1)

    direction = 1
    setItem()
    findLast()

def createBoardTwo():
    global board, direction, directionTwo
    board.clear()
    for i in range(0, 16, 1):
        board.append([])

    for i in range(0, 16, 1):
        for j in range(0, 16, 1):
            board[i].append(boardPiece())


    board[8][8].changeSnake()
    board[8][8].changeNum(3)
    board[8][8].changeSnakeNum(1)
    board[8][7].changeSnake()
    board[8][7].changeNum(2)
    board[8][7].changeSnakeNum(1)
    board[8][6].changeSnake()
    board[8][6].changeNum(1)
    board[8][6].changeSnakeNum(1)

    board[6][9].changeSnake()
    board[6][9].changeNum(1)
    board[6][9].changeSnakeNum(2)
    board[6][8].changeSnake()
    board[6][8].changeNum(2)
    board[6][8].changeSnakeNum(2)
    board[6][7].changeSnake()
    board[6][7].changeNum(3)
    board[6][7].changeSnakeNum(2)

    setItem()
    findLast()
    direction = 1
    directionTwo = 2

def drawSnake():
    drawGrid()
    drawItem()
    drawScores()
    colour = green
    for i in range(0, 16, 1):
        for j in range(0, 16, 1):
            if board[i][j].getSnake():
                if board[i][j].getSnakeNum() == 1:
                    colour = green
                else:
                    colour = snakeBlue
                radius = int((((smaller * (1 + i) * (28 / 8)) / 60) - ((smaller * i * (28 / 8)) / 60)) / 2)
                xInt = int((smaller / 30) + ((smaller * i * (28 / 8)) / 60) + radius)
                yInt = int((smaller / 30) + ((smaller * j * (28 / 8)) / 60) + radius)

                pygame.draw.circle(SCREEN, colour, (xInt, yInt), radius)
                pygame.draw.circle(SCREEN, black, (xInt, yInt), radius, 1)

    pygame.display.update()

def findLast():
    lastNum = 0
    savedI = -1
    savedJ = -1
    for i in range(0, 16, 1):
        for j in range(0, 16, 1):
            if board[i][j].getNum() > lastNum and board[i][j].getSnakeNum() == 1:
                lastNum = board[i][j].getNum()
                savedI = i
                savedJ = j
            if board[savedI][savedJ].getLastSnake() and board[i][j].getSnakeNum() == 1:
                board[i][j].changeLastSnake(False)


    board[savedI][savedJ].changeLastSnake(True)

    lastNum = -1

    if twoPlayers :
        for i in range(0, 16, 1):
            for j in range(0, 16, 1):
                if board[i][j].getNum() > lastNum and board[i][j].getSnakeNum() == 2:
                    lastNum = board[i][j].getNum()
                    savedI = i
                    savedJ = j
                if board[savedI][savedJ].getLastSnake() and board[i][j].getSnakeNum() == 2:
                    board[i][j].changeLastSnake(False)

        board[savedI][savedJ].changeLastSnake(True)

def moveSnakePos(addPiece):
    global gameOver, gotItem, scoreOne, scoreTwo, twoLoses

    #For player one
    for i in range(0, 16, 1):
        for j in range(0, 16, 1):
            if board[i][j].getNum() == 1 and board[i][j].getSnakeNum() == 1:
                #Going up
                if direction == 1:
                    if j != 0 and not board[i][j - 1].getSnake():
                        board[i][j - 1].changeSnake()
                        board[i][j - 1].changeNum(0)
                        board[i][j - 1].changeSnakeNum(1)
                    else:
                        gameOver = True
                if direction == 2:
                    if j != 15 and not board[i][j + 1].getSnake():
                        board[i][j + 1].changeSnake()
                        board[i][j + 1].changeNum(0)
                        board[i][j + 1].changeSnakeNum(1)
                    else:
                        gameOver = True
                if direction == 3:
                    if i != 15 and not board[i + 1][j].getSnake():
                        board[i + 1][j].changeSnake()
                        board[i + 1][j].changeNum(0)
                        board[i + 1][j].changeSnakeNum(1)
                    else:
                        gameOver = True
                if direction == 4:
                    if i != 0 and not board[i - 1][j].getSnake():
                        board[i - 1][j].changeSnake()
                        board[i - 1][j].changeNum(0)
                        board[i - 1][j].changeSnakeNum(1)
                    else:
                        gameOver = True


    # For player two
    if twoPlayers and not gameOver:
        for i in range(0, 16, 1):
            for j in range(0, 16, 1):
                if board[i][j].getNum() == 1 and board[i][j].getSnakeNum() == 2:
                    # Going up
                    if directionTwo == 1:
                        if j != 0 and not board[i][j - 1].getSnake():
                            board[i][j - 1].changeSnake()
                            board[i][j - 1].changeNum(0)
                            board[i][j - 1].changeSnakeNum(2)
                        else:
                            gameOver = True
                            twoLoses = True
                    if directionTwo == 2:
                        if j != 15 and not board[i][j + 1].getSnake():
                            board[i][j + 1].changeSnake()
                            board[i][j + 1].changeNum(0)
                            board[i][j + 1].changeSnakeNum(2)
                        else:
                            gameOver = True
                            twoLoses = True
                    if directionTwo == 3:
                        if i != 15 and not board[i + 1][j].getSnake():
                            board[i + 1][j].changeSnake()
                            board[i + 1][j].changeNum(0)
                            board[i + 1][j].changeSnakeNum(2)
                        else:
                            gameOver = True
                            twoLoses = True
                    if directionTwo == 4:
                        if i != 0 and not board[i - 1][j].getSnake():
                            board[i - 1][j].changeSnake()
                            board[i - 1][j].changeNum(0)
                            board[i - 1][j].changeSnakeNum(2)
                        else:
                            gameOver = True
                            twoLoses = True


    oneIncrease = False
    twoIncrease = False
    for i in range(0, 16, 1):
        for j in range(0, 16, 1):
            if board[i][j].getSnake() and board[i][j].getItem() and board[i][j].getSnakeNum() == 1:
                gotItem = True
                addPiece = True
                scoreOne += 1
                oneIncrease = True
                board[i][j].changeItem(False)
            if board[i][j].getSnake() and board[i][j].getItem() and board[i][j].getSnakeNum() == 2:
                gotItem = True
                addPiece = True
                twoIncrease = True
                scoreTwo += 1
                board[i][j].changeItem(False)

    for i in range(0, 16, 1):
        for j in range(0, 16, 1):
            if board[i][j].getSnakeNum() == 1:
                tempNum = board[i][j].getNum()
                board[i][j].changeNum(tempNum + 1)
            if board[i][j].getSnakeNum() == 2:
                tempNum = board[i][j].getNum()
                board[i][j].changeNum(tempNum + 1)



    findLast()

    for i in range(0, 16, 1):
        for j in range(0, 16, 1):
            if not addPiece:
                if board[i][j].getLastSnake() and board[i][j].getSnakeNum() == 1 and not oneIncrease:
                    board[i][j].removeSnake()
                if board[i][j].getLastSnake() and board[i][j].getSnakeNum() == 2 and not twoIncrease:
                    board[i][j].removeSnake()

if __name__ == '__main__':
    main()
