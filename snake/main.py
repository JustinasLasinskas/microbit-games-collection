from microbit import *
import random

display.clear()

# init parameters
gameOn = False
score = 0
snake = [[1,0],[1,1]]
headCoord = [1,1]
dirX = 0
dirY = 1

def genFood(snake):
    while True:
        foodCoord = [random.randrange(0,5),random.randrange(0,5)]
        if foodCoord in snake:
            foodCoord = [random.randrange(0,5),random.randrange(0,5)]       
        else:
            return foodCoord           
        
foodCoord = genFood(snake)

startImage = "00000:06060:66066:06060:00000"
startCounter = ["06660:00060:06660:00060:06660","06660:00060:06660:06000:06660","00600:06600:00600:00600:06660"]

#main game loop while game is in menu
while not gameOn:

    display.show(Image(startImage))

    if button_a.is_pressed() and button_b.is_pressed():
        gameOn = True
        sleep(400)
       
#start game counter screen
for noCount in startCounter:
    display.show(Image(noCount))
    sleep(1000)
    display.clear()

#main game loop while game is started
while gameOn:

    #inputs
    if button_a.is_pressed() and dirY == 1:
        dirX, dirY = 1, 0
    elif button_a.is_pressed() and dirX == 1:
        dirX, dirY = 0, -1
    elif button_a.is_pressed() and dirY == -1:
        dirX, dirY = -1, 0
    elif button_a.is_pressed() and dirX == -1:
        dirX, dirY = 0, 1
    if button_b.is_pressed() and dirY == 1:
        dirX, dirY = -1, 0
    elif button_b.is_pressed() and dirX == 1:
        dirX, dirY = 0, 1
    elif button_b.is_pressed() and dirY == -1:
        dirX, dirY = 1, 0
    elif button_b.is_pressed() and dirX == -1:
        dirX, dirY = 0, -1
    
    #move snake
    headCoord = [snake[-1][0]+dirX,snake[-1][1]+dirY]
    snake.append(headCoord)    

    #eat food
    if snake[-1] == foodCoord:
        foodCoord = genFood(snake)
        score += 1
    else:
        snake.pop(0)

    #check game over
    if (snake[-1][0] > 4 or snake[-1][0] < 0) or (snake[-1][1] > 4 or snake[-1][1] < 0) or (snake[-1] in snake[:-1]):
        gameOn = False
        break

    #update game
    display.clear()
    for i in snake:        
        display.set_pixel(i[0],i[1],7 if i == headCoord else 5)
    display.set_pixel(foodCoord[0],foodCoord[1],9)

    # "frame counter"
    sleep(round(600,0))    

display.clear()
display.show(Image("90009:09090:00900:09090:90009"))
sleep(1000)    

display.scroll("Score: " + str(score))
reset()