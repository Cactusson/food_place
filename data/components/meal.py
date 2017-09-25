import pygame as pg

from .. import prepare
from .label import Label


class Meal(pg.sprite.Sprite):
    def __init__(self, center, entry, number):
        pg.sprite.Sprite.__init__(self)
        self.number = number
        self.image = prepare.GFX['other']['meal{}'.format(self.number)]
        self.rect = self.image.get_rect(center=center)
        self.entry = entry
        self.state = 'STAND'
        self.mark = None  # marks are created in Waiter

    def __str__(self):
        return "MEAL {}".format(self.number)

    def make_image(self):
        size = 25
        image = pg.Surface((size, size)).convert()
        image.fill(pg.Color('white'))
        label = Label(20, str(self.number), center=(size // 2, size // 2))
        image.blit(label.image, label.rect)
        return image

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.mark:
            self.mark.draw(surface)
