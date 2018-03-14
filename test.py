from sense_hat import SenseHat
import time
import random

sense = SenseHat()

#sense.low_light = True

def c():
    return [
        random.randint(0,31),
        random.randint(0,31),
        random.randint(0,31)
    ]

def g():
    return 1

try:
    gamma = range(0, 32)
    pixel = [
        c(),c(),c(),c(),c(),c(),c(),c(),
        c(),c(),c(),c(),c(),c(),c(),c(),
        c(),c(),c(),c(),c(),c(),c(),c(),
        c(),c(),c(),c(),c(),c(),c(),c(),
        c(),c(),c(),c(),c(),c(),c(),c(),
        c(),c(),c(),c(),c(),c(),c(),c(),
        c(),c(),c(),c(),c(),c(),c(),c(),
        c(),c(),c(),c(),c(),[1,0,0],[31,0,0],c()
    ]
    pixel = map(lambda c: map(lambda v: v*8, c), pixel)
    #gamma.reverse()
    sense.gamma = gamma
    sense.set_pixels(pixel)
    time.sleep(5)
    sense.gamma_reset()
    sense.clear()
except KeyboardInterrupt:
    sense.gamma_reset()
    sense.clear()