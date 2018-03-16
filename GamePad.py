# -----------------------------------------------------------------------------
# Gamepad
# -----------------------------------------------------------------------------
import time
import sys
from enum import Enum
from evdev import InputDevice, list_devices, ecodes, categorize

class GAMEPAD_SENSE_BUTTON (Enum) :
    UP = 103
    DOWN = 108
    LEFT = 105
    RIGTH = 106
    MIDDLE = 28

class GAMEPAD_BUTTON (Enum) : 
    X = 288
    A = 289
    B = 290
    Y = 291
    LEFT_TRIGGER = 292
    RIGHT_TRIGGER = 293
    SELECT = 296
    START = 297

class GAMEPAD_AXIS_RANGE (Enum) : 
    MIN = 0
    MID = 127
    MAX = 255

class GAMEPAD_AXIS (Enum) : 
    X = 0
    Y = 1

class GAMEPAD_AXIS_DIRECTION :
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGTH = 3

class GamePad:

    device = None

    pressed = {

        GAMEPAD_AXIS_DIRECTION.UP: False,
        GAMEPAD_AXIS_DIRECTION.DOWN: False,
        GAMEPAD_AXIS_DIRECTION.LEFT: False,
        GAMEPAD_AXIS_DIRECTION.RIGTH: False,

        GAMEPAD_BUTTON.X: False,
        GAMEPAD_BUTTON.A: False,
        GAMEPAD_BUTTON.B: False,
        GAMEPAD_BUTTON.Y: False,
        GAMEPAD_BUTTON.LEFT_TRIGGER: False,
        GAMEPAD_BUTTON.RIGHT_TRIGGER: False,
        GAMEPAD_BUTTON.SELECT: False,
        GAMEPAD_BUTTON.START: False
    }

    def __init__(self):
        try:
            time.sleep(1)
            print('Select Gamepad')
            foundGamepad = True

            devices = [InputDevice(fn) for fn in list_devices()]
            
            for num, dev in enumerate(devices):
                print(dev.name)

            print('Press any button of these gamepads')

            while True:
                for device in devices:
                    try:
                        for event in device.read():
                            self.device = device
                            time.sleep(1)
                            return
                    except IOError:
                        continue                 
        except OSError:
            foundGamepad = False

        if not(foundGamepad):
            print('Gamepad not found. Aborting ...')
            sys.exit()

    def update (self):
        if self.device.name == "USB Gamepad ":
            self.updateUSBGamepad()
        if self.device.name == "Raspberry Pi Sense HAT Joystick":
            self.updateRaspberryPiSenseHatJoystick()

    def updateRaspberryPiSenseHatJoystick (self):
        try:
            for event in self.device.read():
                if event.type == ecodes.EV_KEY:
                    if GAMEPAD_SENSE_BUTTON(event.code) == GAMEPAD_SENSE_BUTTON.UP :
                        self.pressed[GAMEPAD_AXIS_DIRECTION.UP] = event.value == 1
                    if GAMEPAD_SENSE_BUTTON(event.code) == GAMEPAD_SENSE_BUTTON.DOWN :
                        self.pressed[GAMEPAD_AXIS_DIRECTION.DOWN] = event.value == 1
                    if GAMEPAD_SENSE_BUTTON(event.code) == GAMEPAD_SENSE_BUTTON.LEFT :
                        self.pressed[GAMEPAD_AXIS_DIRECTION.LEFT] = event.value == 1
                    if GAMEPAD_SENSE_BUTTON(event.code) == GAMEPAD_SENSE_BUTTON.RIGTH :
                        self.pressed[GAMEPAD_AXIS_DIRECTION.RIGTH] = event.value == 1
                    if GAMEPAD_SENSE_BUTTON(event.code) == GAMEPAD_SENSE_BUTTON.MIDDLE :
                        self.pressed[GAMEPAD_BUTTON.B] = event.value == 1
        except IOError:
            return
        return

    def updateUSBGamepad (self):
        try:
            for event in self.device.read():
                if event.type == ecodes.EV_KEY:
                    self.pressed[GAMEPAD_BUTTON(event.code)] = event.value == 1
                if event.type == ecodes.EV_ABS:
                    if GAMEPAD_AXIS(event.code) == GAMEPAD_AXIS.X:
                        if GAMEPAD_AXIS_RANGE(event.value) == GAMEPAD_AXIS_RANGE.MIN:
                            self.pressed[GAMEPAD_AXIS_DIRECTION.LEFT] = True
                        if GAMEPAD_AXIS_RANGE(event.value) == GAMEPAD_AXIS_RANGE.MID:
                            self.pressed[GAMEPAD_AXIS_DIRECTION.LEFT] = False
                            self.pressed[GAMEPAD_AXIS_DIRECTION.RIGTH] = False
                        if GAMEPAD_AXIS_RANGE(event.value) == GAMEPAD_AXIS_RANGE.MAX:
                           self.pressed[GAMEPAD_AXIS_DIRECTION.RIGTH] = True
                    if GAMEPAD_AXIS(event.code) == GAMEPAD_AXIS.Y:
                        if GAMEPAD_AXIS_RANGE(event.value) == GAMEPAD_AXIS_RANGE.MIN:
                            self.pressed[GAMEPAD_AXIS_DIRECTION.UP] = True
                        if GAMEPAD_AXIS_RANGE(event.value) == GAMEPAD_AXIS_RANGE.MID:
                            self.pressed[GAMEPAD_AXIS_DIRECTION.UP] = False
                            self.pressed[GAMEPAD_AXIS_DIRECTION.DOWN] = False
                        if GAMEPAD_AXIS_RANGE(event.value) == GAMEPAD_AXIS_RANGE.MAX:
                            self.pressed[GAMEPAD_AXIS_DIRECTION.DOWN] = True
        except IOError:
            return
        return
