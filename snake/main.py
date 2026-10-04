from microbit import *
import random

display.clear()

# init parameters
game_on = False
score = 0
snake = [[1,0],[1,1]]
head_coord = [1,1]
dir_x = 0
dir_y = 1

def gen_food(snake):
    while True:
        food_coord = [random.randrange(0,5),random.randrange(0,5)]
        if food_coord in snake:
            food_coord = [random.randrange(0,5),random.randrange(0,5)]       
        else:
            return food_coord           
        
food_coord = gen_food(snake)

start_image = "00000:06060:66066:06060:00000"
start_counter = ["06660:00060:06660:00060:06660","06660:00060:06660:06000:06660","00600:06600:00600:00600:06660"]

#main game loop while game is in menu
while not game_on:

    display.show(Image(start_image))

    if button_a.is_pressed() and button_b.is_pressed():
        game_on = True
        sleep(400)
       
#start game counter screen
for no_count in start_counter:
    display.show(Image(no_count))
    sleep(1000)
    display.clear()

#main game loop while game is started
while game_on:

    #inputs
    if button_a.is_pressed() and dir_y == 1:
        dir_x, dir_y = 1, 0
    elif button_a.is_pressed() and dir_x == 1:
        dir_x, dir_y = 0, -1
    elif button_a.is_pressed() and dir_y == -1:
        dir_x, dir_y = -1, 0
    elif button_a.is_pressed() and dir_x == -1:
        dir_x, dir_y = 0, 1
    if button_b.is_pressed() and dir_y == 1:
        dir_x, dir_y = -1, 0
    elif button_b.is_pressed() and dir_x == 1:
        dir_x, dir_y = 0, 1
    elif button_b.is_pressed() and dir_y == -1:
        dir_x, dir_y = 1, 0
    elif button_b.is_pressed() and dir_x == -1:
        dir_x, dir_y = 0, -1
    
    #move snake
    head_coord = [snake[-1][0]+dir_x,snake[-1][1]+dir_y]
    snake.append(head_coord)    

    #eat food
    if snake[-1] == food_coord:
        food_coord = gen_food(snake)
        score += 1
    else:
        snake.pop(0)

    #check game over
    if (snake[-1][0] > 4 or snake[-1][0] < 0) or (snake[-1][1] > 4 or snake[-1][1] < 0) or (snake[-1] in snake[:-1]):
        game_on = False
        break

    #update game
    display.clear()
    for i in snake:        
        display.set_pixel(i[0],i[1],7 if i == head_coord else 5)
    display.set_pixel(food_coord[0],food_coord[1],9)

    # "frame counter"
    sleep(round(600,0))    

display.clear()
display.show(Image("90009:09090:00900:09090:90009"))
sleep(1000)    

display.scroll("Score: " + str(score))
reset()