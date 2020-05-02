import pygame
import random

pygame.init() #Initilizes Pygame

#sets colours
white = (255,255,255)
blue = (0,0,255)
red = (255,0,0)
green = (0,255,0)


gameDisplay = pygame.display.set_mode((600,800)) #Creates window with resolution
pygame.display.set_caption("Arkanoid Game by Gurdit Rehal")#Sets window caption
clock = pygame.time.Clock() #Initilizes the clock

multi = 1 #a multiplier to increase speed of the paddle the longer it is pressed with the effect of increasing bounce angle the faster it is

#sets position for paddle
xPaddle = 225
yPaddle = 770

#sets positon for ball
xBall = 285
yBall = 700

#sets speed for paddle
xPaddleChange = 0

#sets speed for ball
xBallChange = -5
yBallChange = -5

def paddle(x,y):
    #paddle is a rectangle with dimensions: 150x20
    pygame.draw.rect(gameDisplay, blue, [x,y,150, 20])

def ball(x,y):
    #"ball" is a 30x30 square
    pygame.draw.rect(gameDisplay, green, [x,y,30, 30])

def brickArrayGen():
    #Creates the 100*50 bricks at the beginning of the game - each element in the array contains the position of each brick
    brickArr = []
    
    y = 100
    ##Nested loop creates array of bricks
    while y <= 400:
        x = 0
        while x <= 500:

            #if (x == 0) or (x == 200) or (x == 500):
             #   x+=100
            #else:
            brickArr.append((x,y))
            x += 100
        y += 50

    return brickArr

def brickCollision(x,y, brickArr): #x,y are xBall and yBall
    #This function detects a collision and returns true or false and manipulates brickArr if a collision is detected
    collision = False

    i = 0
    while (i < len(brickArr)) and (collision == False):
        #if (yPaddle == (yBall + 30)) and (((xBall + 30)> xPaddle) and (xBall <(xPaddle + 150))):
        if ((x + 30)>=brickArr[i][0]) and (x <= (brickArr[i][0]+100)) and ((y + 30) >= brickArr[i][1]) and (y <= (brickArr[i][1]+ 50)):
            collision = True
            brickArr.pop(i) #removes that brick from array
        else:
            i += 1
    return collision, brickArr
        
def brickDraw(brickArr):
    for coord in brickArr:
        pygame.draw.rect(gameDisplay, red, [coord[0],coord[1],100, 50])
    
    
brickArr = brickArrayGen()

end = False
score = 0
while end == False:
    
    for event in pygame.event.get():
        ###Allows to exit program using 'x'
        if event.type == pygame.QUIT:
            end = True
            
        ###Checks if a key has been pressed
        elif event.type == pygame.KEYDOWN:
            multi += 1.5 #increase multi when a key is pressed
            ###Checks which key was pressed and make corresponding change
            if event.key == pygame.K_LEFT:
                xPaddleChange = -5
            if event.key == pygame.K_RIGHT:
                xPaddleChange = 5

        ###Checks if key has been released
        elif event.type == pygame.KEYUP:
            multi = 1 #resets multi when key is released
            ###Resets x to 0 to stop movement
            if (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT):
                xPaddleChange = 0

    #handles ball touching bricks
    collision, brickArr = brickCollision(xBall, yBall, brickArr)
    if collision == True:
        score += 1
        if yBallChange < 0:
            yBallChange = yBallChange * -1
        else:
            xBallChange = xBallChange * -1 #if ball was already moving down when colliding with a brick (e.g. after collding with another brick beforehand)
        

    #computes new location of ball
    xBall += xBallChange
    yBall += yBallChange

    #computes location of paddle
    xPaddle += (xPaddleChange * multi)


    ##handles ball leaving walls (sides of screen)
    if (xBall <= 0) or(xBall >= 575):
        xBallChange = xBallChange * -1 #inverts x direction if colliding with side of screen
    ##handles ball touching ceiling
    if (yBall <= 0):
        yBallChange = yBallChange * -1 #inverts y direction if colliding with ceiling

    ##handles ball going below the paddle
    if yBall > 790:
        end = True
    
    ##handles paddle touching walls
    if xPaddle < 0:
        multi = 1 #resets multi when collision occurs with wall
        xPaddle = 0
    elif xPaddle > 450:
        multi = 1
        xPaddle = 450

    ##handles ball touching paddle
    if (yPaddle == (yBall + 30)) and (((xBall + 30)> xPaddle) and (xBall <(xPaddle + 150))):
        yBall -= 25 #moves ball up to avoid overlap
        yBallChange = yBallChange * -1 #inverts y direction if colliding with ceiling

        #multiplies x speed of ball after collision with moving paddle
        xBall -= xBallChange
        xBall += (xBallChange * multi)


    #re-generates the bricks once they've all been destroyed
    if brickArr == []:
        brickArr = brickArrayGen()

      
    gameDisplay.fill(white)
    paddle(xPaddle,yPaddle)
    ball(xBall,yBall)
    brickDraw(brickArr)

    pygame.display.update()
    clock.tick(60)        

pygame.quit() #Quits PyGame
print("Score: " + str(score))
input("Press enter to continue")
quit()
