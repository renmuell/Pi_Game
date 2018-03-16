# -----------------------------------------------------------------------------
# World
# -----------------------------------------------------------------------------

X = [8,8,8]
_ = [0,0,0]
D = [174,63,63]

class World:

    room_1 = [
        X,X,X,X,X,X,X,X,
        D,_,_,_,_,_,_,X,
        X,_,_,_,_,_,_,X,
        X,_,_,_,_,_,_,X,
        X,_,X,X,_,_,_,X,
        X,_,_,X,_,_,_,X,
        X,_,_,X,_,_,_,X,
        X,X,X,X,X,X,X,X
    ]

    room_2 = [
        X,X,X,X,X,X,X,X,
        X,_,_,_,_,_,_,D,
        X,_,_,_,_,_,_,X,
        X,_,_,X,X,_,_,X,
        X,_,_,X,X,_,_,X,
        X,_,_,_,_,_,_,X,
        X,_,_,_,_,_,_,X,
        X,X,X,X,X,X,X,X
    ]

    world = None

    game = None

    def __init__(self, game):
        self.game = game
        self.world = self.room_1

    def draw (self):
        self.game.screen.set(list(self.world))

    def update(self):
        x = int(round((self.game.player.x)))
        y = int(round((self.game.player.y)))

        if self.world[(((y-1)*8) + (x-1))] == D:
            if self.world == self.room_1:
                self.world = self.room_2
                self.game.player.x = 7
                self.game.player.y = 2
            else:
                self.world = self.room_1
                self.game.player.x = 2
                self.game.player.y = 2

    def collide (self, x, y):

        # Outside
        if (x < 1 or x > 8  or y < 1 or y > 8) :
            return True

        x = int(round((x)))
        y = int(round((y)))
        return self.world[(((y-1)*8) + (x-1))] == X
