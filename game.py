#!/usr/bin/python
import sys
import time
from GamePad import GamePad, GAMEPAD_BUTTON, GAMEPAD_AXIS_DIRECTION
from sense_hat import SenseHat

print("Press Ctrl-C to quit")
time.sleep(1)

gamepad = GamePad()

# -----------------------------------------------------------------------------
# Screen
# -----------------------------------------------------------------------------

sense = SenseHat()

sense.low_light = True



r = [255, 0, 0]
b = [0, 0, 255]
g = [0, 255, 0]
E = [0,0,0]
O = [8,8,8]

t = [78,205,196]
rP = [255,107,107]
gP = [199,244,100]
ye = [255,247,114]

def ShowScreen(player_x, player_y, playerDirectionX, playerDirectionY, projectiles):
    global sense
    player_x = int(round((player_x)))
    player_y = int(round((player_y)))
    pixel = [
        O,O,O,O,O,O,O,O,
        E,E,E,E,E,E,E,O,
        O,E,E,E,E,E,E,O,
        O,E,E,E,E,E,E,O,
        O,E,O,O,E,E,E,O,
        O,E,E,O,E,E,E,O,
        O,E,E,O,E,E,E,O,
        O,O,O,O,O,O,O,O
    ]
    player_look_x = player_x + playerDirectionX
    player_look_y = player_y + playerDirectionY

    pixel[(((player_y-1)*8) + (player_x-1))] = t
    if (player_look_x>0 and player_look_x < 9  and player_look_y > 0 and player_look_y <9) :
        pixel[(((player_look_y-1)*8) + (player_look_x-1))] = ye


    for projectile in projectiles:
        if (projectile[4]) :
            p_x = int(round(projectile[0]))
            p_y = int(round(projectile[1]))
            pixel[(((p_y-1)*8) + (p_x-1))] = gP

    # red shift test
    #pixel = map(lambda c: [ c[0]*8 if c[0]*8 < 256 else 255 ,c[1],c[2]], pixel)

    sense.set_pixels(pixel)

# -----------------------------------------------------------------------------
# Player
# -----------------------------------------------------------------------------

player_x = 1
player_y = 1
playerSpeed = 10
playerDirectionX = 1
playerDirectionY = 0
projectiles = []
projectile_speed = 10

# -----------------------------------------------------------------------------
# Logic
# -----------------------------------------------------------------------------

def update_game (dt) :
    global player_x
    global playerSpeed
    global player_y
    global playerDirectionX
    global playerDirectionY
    global game_is_running
    global gamepad

    for projectile in projectiles:
        if (projectile[4]) :
            projectile[0] += ((projectile[2]*projectile_speed)*dt)
            projectile[1] += ((projectile[3]*projectile_speed)*dt)
            if (projectile[0]<1 or projectile[0] > 8  or projectile[1]<1 or projectile[1] > 8) :
                projectile[4] = False

    gamepad.update()

    if (gamepad.pressed[GAMEPAD_AXIS_DIRECTION.DOWN]):
        player_y += (playerSpeed*dt)
        playerDirectionY = 1
        playerDirectionX = 0
    if (gamepad.pressed[GAMEPAD_AXIS_DIRECTION.UP]) : 
        player_y -= (playerSpeed*dt)
        playerDirectionY = -1
        playerDirectionX = 0

    if (player_y < 1) :
        player_y = 1
    if (player_y > 8) :
        player_y = 8
    
    if (gamepad.pressed[GAMEPAD_AXIS_DIRECTION.LEFT]):
        player_x -= (playerSpeed*dt)
        playerDirectionY = 0
        playerDirectionX = -1
    if (gamepad.pressed[GAMEPAD_AXIS_DIRECTION.RIGTH]) : 
        player_x += (playerSpeed*dt)
        playerDirectionY = 0
        playerDirectionX = 1

    if (gamepad.pressed[GAMEPAD_BUTTON.LEFT_TRIGGER]) :
        player_x -= (playerSpeed*dt)
    if (gamepad.pressed[GAMEPAD_BUTTON.RIGHT_TRIGGER]) :
        player_x += (playerSpeed*dt)

    if (player_x < 1) :
        player_x = 1
    if (player_x > 8) :
        player_x = 8

    if (gamepad.pressed[GAMEPAD_BUTTON.B]) :
        projectiles.append([
            player_x,
            player_y,
            playerDirectionX,
            playerDirectionY,
            True
        ])

    if (gamepad.pressed[GAMEPAD_BUTTON.START]) :
        game_is_running = False

# -----------------------------------------------------------------------------
# Draw
# -----------------------------------------------------------------------------

def display_game () :
    global player_x
    global player_y
    global playerDirectionX
    global playerDirectionY
    global projectiles
    ShowScreen(player_x, player_y, playerDirectionX, playerDirectionY, projectiles)

# -----------------------------------------------------------------------------
# Game
# -----------------------------------------------------------------------------

print("GO!")

game_is_running = True
FRAMES_PER_SECOND = 25
lastFrameTime = time.time()

try:
    while game_is_running :
        currentTime = time.time()
        dt = currentTime - lastFrameTime
        
        sleepTime = 1./FRAMES_PER_SECOND - (currentTime - lastFrameTime)

        if sleepTime > 0:
            time.sleep(sleepTime)

        update_game(dt)
        display_game()

        lastFrameTime = currentTime
    sense.clear()
except KeyboardInterrupt:
    sense.clear()
    sys.exit()
