import pygame as pg

from .. import prepare
from .label import Label


class Order(pg.sprite.Sprite):
    def __init__(self, number):
        pg.sprite.Sprite.__init__(self)
        self.number = number
        self.image = pg.transform.scale(prepare.GFX['other']['order'],
                                        (35, 50))
        # self.image = self.make_image()
        self.rect = self.image.get_rect()
        self.state = 'STAND'

    def __str__(self):
        return "ORDER {}".format(self.number)

    def make_image(self):
        size = 25
        image = pg.Surface((size, size)).convert()
        image.fill(pg.Color('white'))
        label = Label(20, str(self.number), center=(size // 2, size // 2))
        image.blit(label.image, label.rect)
        return image

    def draw(self, surface):
        surface.blit(self.image, self.rect)
