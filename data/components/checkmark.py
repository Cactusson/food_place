from .. import prepare, tools


class Checkmark:
    def __init__(self, center):
        self.image = prepare.GFX['gui']['checkmark']
        self.image = tools.colorize(self.image, (0, 200, 0))
        self.rect = self.image.get_rect(center=center)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
