# -----------------------------------------------------------------------------
# Bullet
# -----------------------------------------------------------------------------

class Bullet:

    alive = True
    x = 0
    y = 0
    
    direction_x = 1
    direction_y = 0

    color = [190,41,236]
    speed = 10

    game = None

    def __init__(self, game, x, y, dir_x, dir_y):
        self.x = x
        self.y = y
        self.direction_x = dir_x
        self.direction_y = dir_y
        self.game = game

    def update (self, dt):
        
        self.x += ((self.direction_x * self.speed) * dt)
        self.y += ((self.direction_y * self.speed) * dt)

    def draw (self):
        self.game.screen.set_pixel(self.x, self.y, self.color)

        if (self.game.world.collide(self.x, self.y)) :
            self.alive = False
