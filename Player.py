# -----------------------------------------------------------------------------
# Player
# -----------------------------------------------------------------------------

from GamePad import GAMEPAD_BUTTON, GAMEPAD_AXIS_DIRECTION
from Bullet import Bullet

class Player:

    game = None
    
    alive = True

    x = 2
    y = 2

    speed = 10

    color = [78, 205, 196]
    
    direction_x = 1
    direction_y = 0
    look_color = [255,247,114]
    walking = False

    def __init__(self, game):
        self.game = game

    def update (self, dt):

        if (self.game.gamepad.pressed[GAMEPAD_BUTTON.B]) :
            self.game.entityManager.add(Bullet(
                self.game,
                self.x,
                self.y,
                self.direction_x,
                self.direction_y))

        new_x = self.x
        new_y = self.y

        if (self.game.gamepad.pressed[GAMEPAD_AXIS_DIRECTION.DOWN]):
            if self.direction_y == 1:
                new_y += (self.speed*dt)
            self.direction_y = 1
            self.direction_x = 0
        if (self.game.gamepad.pressed[GAMEPAD_AXIS_DIRECTION.UP]) : 
            if self.direction_y == -1:
                new_y -= (self.speed*dt)
            self.direction_y = -1
            self.direction_x = 0

        if (self.game.gamepad.pressed[GAMEPAD_AXIS_DIRECTION.LEFT]):
            if self.direction_x == -1:
                new_x -= (self.speed*dt)
            self.direction_y = 0
            self.direction_x = -1
        if (self.game.gamepad.pressed[GAMEPAD_AXIS_DIRECTION.RIGTH]) : 
            if self.direction_x == 1:
                new_x += (self.speed*dt)
            self.direction_y = 0
            self.direction_x = 1

        if (self.game.gamepad.pressed[GAMEPAD_BUTTON.LEFT_TRIGGER]) :
            if self.direction_x == 0 :
                new_x = new_x + ((1 if self.direction_y > 0 else -1) * (self.speed*dt))
            else:
                new_y = new_y + ((1 if self.direction_x < 0 else -1) * (self.speed*dt))
        if (self.game.gamepad.pressed[GAMEPAD_BUTTON.RIGHT_TRIGGER]) :
            if self.direction_x == 0 :
                new_x = new_x + ((1 if self.direction_y < 0 else -1) * (self.speed*dt))
            else:
                new_y = new_y + ((1 if self.direction_x > 0 else -1) * (self.speed*dt))

        if (self.game.world.collide(new_x, new_y) == False) :
            self.x = new_x 
            self.y = new_y
            self.walking = True
        else:
            self.walking = False

    def draw (self):
        self.game.screen.set_pixel(self.x, self.y, self.color)

        look_x = int(round(self.x + self.direction_x))
        look_y = int(round(self.y + self.direction_y))

        if (look_x>0 and look_x < 9 and look_y > 0 and look_y <9) :
            self.game.screen.set_pixel(look_x, look_y, self.look_color)
