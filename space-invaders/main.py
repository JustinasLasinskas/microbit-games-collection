from microbit import *
import random

# game speed, milliseconds per frame
FRAME = 80

# init parameters
game_on = False
score = 0
wave = 0
aliens = []
alien_dir = 1
alien_step = 0
trips = 0
move_every = 12
bomb_every = 40
frame_count = 1
bullet_x = -1
bullet_y = -1
bomb_x = -1
bomb_y = -1
ship_x = 2

def gen_aliens():
    # starting formation, three rows of four invaders
    fleet = []
    for row in range(3):
        for col in range(4):
            fleet.append([col, row])
    return fleet

def beep(melody):
    # short sound effect, skipped on devices without a buzzer
    try:
        music.play([getattr(music.Note, note) for note in melody])
    except:
        pass

def wait_frames(frames):
    # hold the screen for a number of frames
    for frame in range(frames):
        sleep(FRAME)

def draw():
    display.clear()
    for alien in aliens:
        display.set_pixel(alien[0], alien[1], 8)
    if bullet_y >= 0:
        display.set_pixel(bullet_x, bullet_y, 3)
    if bomb_y >= 0:
        display.set_pixel(bomb_x, bomb_y, 2)
    display.set_pixel(ship_x, 4, 4)

def explode(x, y, colour):
    # flash a burst of pixels on top of the game where something was hit
    burst = [[0, 0], [1, 0], [-1, 0], [0, 1], [0, -1]]
    for frame in range(4):
        draw()
        for pixel in burst:
            if 0 <= x + pixel[0] <= 4 and 0 <= y + pixel[1] <= 4:
                display.set_pixel(x + pixel[0], y + pixel[1], colour)
        sleep(FRAME)

aliens = gen_aliens()

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

display.scroll("TILT")
sleep(600)

#main game loop while game is started
while game_on:

    #inputs, tilt the micro:bit to move the ship left or right
    tilt = accelerometer.get_x()
    if tilt is not None:
        if tilt < -200:
            ship_x -= 1
        elif tilt > 200:
            ship_x += 1
        ship_x = max(0, min(4, ship_x))

    #fire the bullet with either button
    if bullet_y < 0 and (button_a.is_pressed() or button_b.is_pressed()):
        bullet_x = ship_x
        bullet_y = 3
        beep(["C5", "G4"])

    #move the bullet and look for a hit
    if bullet_y >= 0:
        bullet_y -= 1
        if bullet_y < 0 and aliens:
            explode(bullet_x, 0, 1)
            beep(["A4"])
        for alien in aliens:
            if alien[0] == bullet_x and alien[1] == bullet_y:
                aliens.remove(alien)
                score += 1
                explode(bullet_x, bullet_y, 8)
                beep(["G4", "C4"])
                bullet_y = -1
                break

    #send a bomb down from the lowest invader
    if bomb_y < 0 and aliens and frame_count % bomb_every == 0:
        lowest = 0
        for alien in aliens:
            if alien[1] > lowest:
                lowest = alien[1]
        shooters = [a for a in aliens if a[1] == lowest]
        shooter = shooters[random.randrange(len(shooters))]
        bomb_x = shooter[0]
        bomb_y = shooter[1] + 1

    #move the bomb every second frame and look for the ship
    if bomb_y >= 0:
        if bomb_y == 4 and bomb_x == ship_x:
            explode(ship_x, 4, 2)
            beep(["G4", "F4", "E4", "D4", "C4"])
            game_on = False
            break
        if frame_count % 2 == 0:
            bomb_y += 1
            if bomb_y > 4:
                bomb_y = -1

    #move the invaders across the screen, and down on every third trip to the edge
    alien_step += 1
    if alien_step >= move_every and aliens:
        alien_step = 0
        edge = False
        for alien in aliens:
            if alien[0] + alien_dir < 0 or alien[0] + alien_dir > 4:
                edge = True
        if edge:
            alien_dir = -alien_dir
            trips += 1
            if trips >= 3:
                trips = 0
                for alien in aliens:
                    alien[1] += 1
        else:
            for alien in aliens:
                alien[0] += alien_dir

    #check the invaders reached the bottom
    for alien in aliens:
        if alien[1] > 3:
            game_on = False
            break
    if not game_on:
        break

    #start the next wave once the sky is clear
    if not aliens:
        wave += 1
        move_every = max(6, 12 - wave * 2)
        bomb_every = max(20, 40 - wave * 10)
        alien_dir = 1
        alien_step = 0
        trips = 0
        display.scroll("WAVE " + str(wave))
        aliens = gen_aliens()
        wait_frames(5)

    #update game
    draw()

    # "frame counter"
    sleep(FRAME)
    frame_count += 1

display.clear()
display.show(Image("90009:09090:00900:09090:90009"))
sleep(1000)

display.scroll("Score: " + str(score))
reset()