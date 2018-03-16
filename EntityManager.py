# -----------------------------------------------------------------------------
# EntityManager
# -----------------------------------------------------------------------------

class EntityManager:

    enitites = []

    def add (self, entity):
        self.enitites.append(entity)

    def remove (self, entity):
        self.enitites.remove(entity)

    def update (self, dt):
        for entity in self.enitites:
            if (entity.alive):
                entity.update(dt)
            else:
                self.enitites.remove(entity)

    def draw (self):
        for entity in self.enitites:
            if (entity.alive):
                entity.draw()
