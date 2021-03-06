import pygame
from pygame.locals import *
import sys
import FileManager
from PIL import Image


# read config file
FileManager.readFile()

# frame per second
fps = 200

scoreSpace = 50  # free space under area to display scores
windowWidth = FileManager.programElements['width']
windowHeight = FileManager.programElements['height']
areaHeight = windowHeight - scoreSpace
lineThickness = FileManager.programElements['lineThickness']  # thickness of lines in program
padSize = 50  # size of game pad
padDistance = 20  # distance from the area edges

# set up the colors
# background color is always black
borderLinesColor = FileManager.programElements['elementsColor']
padColor = FileManager.programElements['padColor']
ballColor = FileManager.programElements['ballColor']
menuColor = FileManager.programElements['menuColor']


# function to draw game area
def drawArea():
    displaySurf.fill((0, 0, 0))
    # draw border lines
    pygame.draw.rect(displaySurf, borderLinesColor, ((0, 0), (windowWidth, areaHeight)), lineThickness * 2)
    # draw center line
    pygame.draw.line(displaySurf, borderLinesColor, ((windowWidth / 2), 0), ((windowWidth / 2), areaHeight),
                     int(lineThickness / 2))


# function to draw pad
def drawPad(pad):
    # stops pad moving too low
    if pad.bottom > areaHeight - lineThickness:
        pad.bottom = areaHeight - lineThickness  # this is the lowest point of area
    # stops pad moving to high
    elif pad.top < lineThickness:
        pad.top = lineThickness  # lineThickness is the highest point of area
    # draw pad
    pygame.draw.rect(displaySurf, padColor, pad)


# draw ball
def drawBall(ball):
    pygame.draw.rect(displaySurf, ballColor, ball)


# function to changing the ball's position
def moveBall(ball, ballDirX, ballDirY, ball_Speed):
    # ball speed tells how many pixels ball is moved
    ball.x += (ballDirX * ball_Speed)
    ball.y += (ballDirY * ball_Speed)
    return ball  # return new ball's position


# function to check the collision with border line
# function returning the new ball's directions
def checkEdgeCollision(ball, ballDirX, ballDirY):
    # if ball reach the top or bottom border, the Y direction is changing to opposite
    if ball.top <= lineThickness or ball.bottom >= (areaHeight - lineThickness):
        ballDirY = ballDirY * -1
    # if ball reach the left or right border line, the X direction is changing to opposite
    if ball.left <= lineThickness or ball.right >= (windowWidth - lineThickness):
        ballDirX = ballDirX * -1
    return ballDirX, ballDirY


# function to change ball direction when is hit by pad
def checkHitBall(ball, pad1, pad2, ballDirX):
    """ ballDir = -1 -> pad1 may hit the ball
        ball is hit when pad1.right >= ball.left, >= is required, because ball can change the speed
        ball.top is lower when pad.top is smaller
        ball.bottom is hither when pad.bottom is bigger
    """
    if ballDirX == -1 and pad1.right >= ball.left and pad1.top <= ball.top and pad1.bottom >= ball.bottom:
        return -1
    # ballDir = 1 -> pad2 may hit the ball
    # ball is hit when pad1.left == ball.right
    elif ballDirX == 1 and pad2.left <= ball.right and pad2.top <= ball.top and pad2.bottom >= ball.bottom:
        return -1
    else:
        return 1


# if ball hits left or right border line, player one gets 1 point
def checkPointScoredPlayerOne(ball, score):
    if ball.right >= windowWidth - lineThickness:
        score += 1
        return score
    else:
        return score


# if ball hits left or right border line, player one gets 1 point
def checkPointScoredPlayerTwo(ball, score):
    if ball.left <= lineThickness:
        score += 1
        return score
    else:
        return score


# Display players score in the bottom of screen
def displayScore(scorePlayerOne, scorePlayerTwo):
    resultSurfOne = basicFont.render('Player 1 = %s' % scorePlayerOne, True, borderLinesColor)
    resultRectOne = resultSurfOne.get_rect()
    resultRectOne = (windowWidth - 150, windowHeight-30)
    displaySurf.blit(resultSurfOne,resultRectOne)

    resultSurfTwo = basicFont.render('Player 2 = %s' % scorePlayerTwo, True, borderLinesColor)
    resultRectTwo = resultSurfTwo.get_rect()
    resultRectTwo = (40, windowHeight - 30)
    displaySurf.blit(resultSurfTwo, resultRectTwo)


def aiPlayer(pad, ball, botLevel):
        if botLevel:
            if pad.centery > ball.y:
                pad.y += - 5
            if pad.centery < ball.y:
                pad.y += 5
            return pad
        else:
            if pad.centery > ball.y:
                pad.y += - 3
            if pad.centery < ball.y:
                pad.y += 3
            return pad


# Pause game and display same features of program
def paused():

    reset = False
    easyLevel = False
    hardLevel = False
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(1)
    # display "Pause" word
    pauseSurf = basicFont.render('Paused', True, menuColor)
    pauseRect = pauseSurf.get_rect()
    pauseRect = (windowWidth/2 + windowWidth/15, windowHeight/4)
    displaySurf.blit(pauseSurf, pauseRect)

    pause = True
    # prepare buttons
    continueButton = pygame.Rect((windowWidth/4, windowHeight/3), (windowWidth/2, windowHeight/7))
    #
    continueSurf = basicFont.render('Continue', True, menuColor)
    continueRect = continueSurf.get_rect()
    continueRect = (windowWidth / 4 + windowWidth/15, windowHeight / 3 + windowHeight/20)
    displaySurf.blit(continueSurf, continueRect)

    resetButton = pygame.Rect((windowWidth/4, windowHeight/2), (windowWidth/2, windowHeight/7))
    resetSurf = basicFont.render('Reset', True, menuColor)
    resetRect = resetSurf.get_rect()
    resetRect = (windowWidth / 4 + windowWidth / 15, windowHeight / 2 + windowHeight / 20)
    displaySurf.blit(resetSurf, resetRect)

    insButton = pygame.Rect((windowWidth / 4, 2 * windowHeight / 3), (windowWidth / 2, windowHeight / 7))
    insSurf = basicFont.render('Instruction', True, menuColor)
    insRect = insSurf.get_rect()
    insRect = (windowWidth / 4 + windowWidth / 15, 2 * windowHeight / 3 + windowHeight / 20)
    displaySurf.blit(insSurf, insRect)

    # display "AI" word
    aiSurf = basicFont.render('AI', True, menuColor)
    aiRect = aiSurf.get_rect()
    aiRect = (windowWidth/17, windowHeight/17)
    displaySurf.blit(aiSurf, aiRect)

    easyButton = pygame.Rect((windowWidth/17, windowHeight/10), (windowWidth/7, windowHeight/13))
    easySurf = basicFont.render('Easy', True, menuColor)
    easyRect = easySurf.get_rect()
    easyRect = (windowWidth/17 + windowWidth/38, windowHeight/10 + windowHeight/38)
    displaySurf.blit(easySurf, easyRect)

    hardButton = pygame.Rect((windowWidth / 17, 2*windowHeight / 10), (windowWidth / 7, windowHeight / 13))
    hardSurf = basicFont.render('Hard', True, menuColor)
    hardRect = hardSurf.get_rect()
    hardRect = (windowWidth / 17 + windowWidth / 38, 2*windowHeight / 10 + windowHeight / 38)
    displaySurf.blit(hardSurf, hardRect)

    noneButton = pygame.Rect((windowWidth / 17, 3 * windowHeight / 10), (windowWidth / 7, windowHeight / 13))
    noneSurf = basicFont.render('None', True, menuColor)
    noneRect = noneSurf.get_rect()
    noneRect = (windowWidth / 17 + windowWidth / 38, 3 * windowHeight / 10 + windowHeight / 38)
    displaySurf.blit(noneSurf, noneRect)

    # pause loop
    while pause:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if continueButton.collidepoint(mouse_pos):
                    pause = False
                if resetButton.collidepoint(mouse_pos):
                    reset = True
                    pause = False
                if insButton.collidepoint(mouse_pos):
                    img = Image.open("PongIns.png")
                    img.show()
                if easyButton.collidepoint(mouse_pos):
                    easyLevel = True
                    hardLevel = False
                if hardButton.collidepoint(mouse_pos):
                    easyLevel = False
                    hardLevel = True
                if noneButton.collidepoint(mouse_pos):
                    easyLevel = False
                    hardLevel = False

        # draw buttons
        pygame.draw.rect(displaySurf, menuColor, continueButton, int(lineThickness / 4))
        pygame.draw.rect(displaySurf, menuColor, resetButton, int(lineThickness / 4))
        pygame.draw.rect(displaySurf, menuColor, insButton, int(lineThickness / 4))
        pygame.draw.rect(displaySurf, menuColor, easyButton, int(lineThickness / 4))
        pygame.draw.rect(displaySurf, menuColor, hardButton, int(lineThickness / 4))
        pygame.draw.rect(displaySurf, menuColor, noneButton, int(lineThickness / 4))
        pygame.display.update()
        clock.tick(fps)
    return reset, easyLevel, hardLevel


def main():  # main function
    pygame.init()  # init the pygame
    global displaySurf

    # font information
    global basicFont, basicFontSize
    basicFontSize = 20
    basicFont = pygame.font.Font('freesansbold.ttf', basicFontSize)
    # clock
    fpsClock = pygame.time.Clock()
    # display window with parameters
    displaySurf = pygame.display.set_mode((windowWidth, windowHeight))
    # set title
    pygame.display.set_caption("PongWWW")

    # set starting positions of ball and pads
    ballX = windowWidth / 2 - lineThickness / 2  # including the thickness of border lines
    ballY = areaHeight / 2 - lineThickness / 2
    playerOnePosition = (areaHeight - padSize) / 2  # position of pad is only vertical
    playerThoPosition = (areaHeight - padSize) / 2

    # players score
    scorePlayerOne = 0
    scorePlayerTwo = 0

    # create the rectangle for pads and ball
    pad1 = pygame.Rect(padDistance, playerOnePosition, lineThickness, padSize)  # create first player pad
    # create second player pad
    pad2 = pygame.Rect(windowWidth - padDistance - lineThickness, playerThoPosition, lineThickness, padSize)
    ball = pygame.Rect(ballX, ballY, lineThickness, lineThickness)  # create the ball

    # draw game elements
    drawArea()
    drawPad(pad1)
    drawPad(pad2)
    drawBall(ball)

    # Ball direction
    ballDirX = -1  # -1 = left, 1 = right
    ballDirY = -1  # -1 = up, 1 = down

    # ball speed
    ballSpeed = 1
    pygame.mouse.set_visible(0)  # make cursor invisible

    # Bot level
    botLevel = False
    botLevelEasy = False
    botLevelHard = False

    reset = False
    # main Loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # second player control with mouse
            elif event.type == MOUSEMOTION:
                mouseX, mouseY = event.pos
                pad2.y = mouseY
            elif event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    reset, botLevelEasy, botLevelHard = paused()
                    if reset:
                        scorePlayerTwo = 0
                        scorePlayerOne = 0
                    pygame.mouse.set_visible(0)  # make cursor invisible after exit pause

        # first player control with keys UP and DOWN
        keys = pygame.key.get_pressed()
        if botLevelEasy or botLevelHard:
            if botLevelEasy:
                botLevel = False
                pad1 = aiPlayer(pad1, ball, botLevel)
            if botLevelHard:
                botLevel = True
                pad1 = aiPlayer(pad1, ball, botLevel)
        else:
            if keys[pygame.K_DOWN]:
                pad1.y += 3
            if keys[pygame.K_UP]:
                pad1.y += -3

        if keys[pygame.K_1]:
            ballSpeed = 1
        if keys[pygame.K_2]:
            ballSpeed = 2
        if keys[pygame.K_3]:
            ballSpeed = 3
        if keys[pygame.K_4]:
            ballSpeed = 4
        if keys[pygame.K_5]:
            ballSpeed = 5
        if keys[pygame.K_6]:
            ballSpeed = 6
        if keys[pygame.K_7]:
            ballSpeed = 7
        if keys[pygame.K_8]:
            ballSpeed = 8
        if keys[pygame.K_9]:
            ballSpeed = 9

        drawArea()
        drawBall(ball)
        drawPad(pad1)
        drawPad(pad2)

        ball = moveBall(ball, ballDirX, ballDirY, ballSpeed)  # new value of ball's position
        ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)

        scorePlayerOne = checkPointScoredPlayerOne(ball, scorePlayerOne)
        scorePlayerTwo = checkPointScoredPlayerTwo(ball, scorePlayerTwo)

        displayScore(scorePlayerOne, scorePlayerTwo)

        ballDirX = ballDirX * checkHitBall(ball, pad1, pad2, ballDirX)  # check ball's direction after hit with pad
        pygame.display.update()
        fpsClock.tick(fps)


if __name__ == "__main__":
    main()
