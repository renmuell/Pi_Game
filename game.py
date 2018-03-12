#!/usr/bin/python
import sys
import time

from sense_hat import SenseHat
from evdev import InputDevice, list_devices, ecodes, categorize
from pprint import pprint

print("Press Ctrl-C to quit")
time.sleep(1)

# -----------------------------------------------------------------------------
# Gamepad
# -----------------------------------------------------------------------------

foundGamepad = True
try:
    gamepad = InputDevice('/dev/input/event0')
except OSError:
    foundGamepad = False

if not(foundGamepad):
    print('USB Gamepad not found. Aborting ...')
    sys.exit()

yBtn = 291
xBtn = 288
aBtn = 289
bBtn = 290

start = 297
select = 296

lTrig = 292
rTrig = 293

axisMin = 0
axisMid = 127
axisMax = 255

axisY = 1
axisX = 0

yBtnPressed = False
xBtnPressed = False
aBtnPressed = False
bBtnPressed = False

startPressed = False
selectPressed = False

lTrigPressed = False
rTrigPressed = False

topPressed = False
bottomPressed = False
leftPressed = False
rightPressed = False

def ReadGamePad ():
    global lTrigPressed
    global rTrigPressed
    global startPressed
    global bottomPressed
    global topPressed
    global leftPressed
    global rightPressed
    global bBtnPressed
    try:
        for event in gamepad.read():
            if event.type == ecodes.EV_KEY:
                if event.value == 1:
                    if event.code == yBtn:
                        yBtnPressed = True
                    if event.code == xBtn:
                        xBtnPressed = True
                    if event.code == aBtn:
                        aBtnPressed = True
                    if event.code == bBtn:
                        bBtnPressed = True
                    if event.code == start:
                        startPressed = True
                    if event.code == select:
                        selectPressed = True
                    if event.code == lTrig:
                        lTrigPressed = True
                    if event.code == rTrig:
                        rTrigPressed = True
                if event.value == 0:
                    if event.code == yBtn:
                        yBtnPressed = False
                    if event.code == xBtn:
                        xBtnPressed = False
                    if event.code == aBtn:
                        aBtnPressed = False
                    if event.code == bBtn:
                        bBtnPressed = False
                    if event.code == start:
                        startPressed = False
                    if event.code == select:
                        selectPressed = False
                    if event.code == lTrig:
                        lTrigPressed = False
                    if event.code == rTrig:
                        rTrigPressed = False 
            if event.type == ecodes.EV_ABS:
                if event.code == axisX:
                    if event.value == axisMin:
                        leftPressed = True
                    if event.value == axisMid:
                        leftPressed = False
                        rightPressed = False
                    if event.value == axisMax:
                       rightPressed = True
                if event.code == axisY:
                    if event.value == axisMin:
                        topPressed = True
                    if event.value == axisMid:
                        topPressed = False
                        bottomPressed = False
                    if event.value == axisMax:
                        bottomPressed = True
    except IOError:
        return
    return

# -----------------------------------------------------------------------------
# Screen
# -----------------------------------------------------------------------------

sense = SenseHat()
sense.low_light = True

r = [255, 0, 0]
b = [0, 0, 255]
g = [0, 255, 0]
O = [0,0,0]

def ShowScreen(player_x, player_y, playerDirectionX, playerDirectionY, projectiles):
    global r
    global O
    global b
    global g
    global sense
    player_x = int(round((player_x)))
    player_y = int(round((player_y)))
    pixel = [
        O,O,O,O,O,O,O,O,
        O,O,O,O,O,O,O,O,
        O,O,O,O,O,O,O,O,
        O,O,O,O,O,O,O,O,
        O,O,O,O,O,O,O,O,
        O,O,O,O,O,O,O,O,
        O,O,O,O,O,O,O,O,
        O,O,O,O,O,O,O,O
    ]
    player_look_x = player_x + playerDirectionX
    player_look_y = player_y + playerDirectionY

    pixel[(((player_y-1)*8) + (player_x-1))] = b
    if (player_look_x>0 and player_look_x < 9  and player_look_y > 0 and player_look_y <9) :
        pixel[(((player_look_y-1)*8) + (player_look_x-1))] = r


    for projectile in projectiles:
        if (projectile[4]) :
            p_x = int(round(projectile[0]))
            p_y = int(round(projectile[1]))
            pixel[(((p_y-1)*8) + (p_x-1))] = g

    sense.set_pixels(pixel)

# -----------------------------------------------------------------------------
# Player
# -----------------------------------------------------------------------------

player_x = 1
player_y = 0
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
    global bottomPressed
    global topPressed
    global rightPressed
    global leftPressed
    global bBtnPressed
    global playerDirectionX
    global playerDirectionY
    global game_is_running
    global rTrigPressed
    global lTrigPressed

    for projectile in projectiles:
        if (projectile[4]) :
            projectile[0] += ((projectile[2]*projectile_speed)*dt)
            projectile[1] += ((projectile[3]*projectile_speed)*dt)
            if (projectile[0]<1 or projectile[0] > 8  or projectile[1]<1 or projectile[1] > 8) :
                projectile[4] = False

    ReadGamePad()

    if (bottomPressed):
        player_y += (playerSpeed*dt)
        playerDirectionY = 1
        playerDirectionX = 0
    if (topPressed) : 
        player_y -= (playerSpeed*dt)
        playerDirectionY = -1
        playerDirectionX = 0
    if (player_y < 1) :
        player_y = 1
    if (player_y > 8) :
        player_y = 8
    
    if (leftPressed):
        player_x -= (playerSpeed*dt)
        playerDirectionY = 0
        playerDirectionX = -1
    if (rightPressed) : 
        player_x += (playerSpeed*dt)
        playerDirectionY = 0
        playerDirectionX = 1
    if (lTrigPressed) :
        player_x -= (playerSpeed*dt)
    if (rTrigPressed) :
        player_x += (playerSpeed*dt)
    if (player_x < 1) :
        player_x = 1
    if (player_x > 8) :
        player_x = 8

    if (bBtnPressed) :
        projectiles.append([
            player_x,
            player_y,
            playerDirectionX,
            playerDirectionY,
            True
        ])

    if (startPressed):
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
