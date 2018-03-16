# -----------------------------------------------------------------------------
# Game
# -----------------------------------------------------------------------------

import sys
import time
from GamePad import GamePad, GAMEPAD_BUTTON, GAMEPAD_AXIS_DIRECTION
from Player import Player
from Screen import Screen
from EntityManager import EntityManager
from World import World

class Game:

    gamepad = None
    player = None
    screen = None
    entityManager = None
    world = None

    FRAMES_PER_SECOND = 25

    game_is_running = False

    def __init__(self):
        print("Press Ctrl-C to quit")

        self.gamepad = GamePad()
        self.screen = Screen()
        self.entityManager = EntityManager();
        self.player = Player(self)
        self.world = World(self)
        self.entityManager.add(self.player)

    def update(self, dt):
  
        self.gamepad.update()

        if (self.gamepad.pressed[GAMEPAD_BUTTON.START]) :
            self.game_is_running = False
            return

        self.world.update()
        self.entityManager.update(dt)

    def draw(self):
        self.screen.clear()
        self.world.draw()
        self.entityManager.draw()
        self.screen.draw()

    def start(self):
        print("GO!")
        self.loop()

    def loop(self):

        self.game_is_running = True

        lastFrameTime = time.time()

        try:
            while self.game_is_running :
                currentTime = time.time()
                dt = currentTime - lastFrameTime
                
                sleepTime = 1./self.FRAMES_PER_SECOND - (currentTime - lastFrameTime)

                if sleepTime > 0:
                    time.sleep(sleepTime)

                self.update(dt)
                self.draw()

                lastFrameTime = currentTime
            self.screen.off()
        except KeyboardInterrupt:
            self.screen.off()
            sys.exit()

try:
    game = Game()
    game.start()
except OSError:
    print('Bye :P')