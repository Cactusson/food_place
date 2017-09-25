import pygame as pg

from .. import prepare


class Bubble(pg.sprite.Sprite):
    def __init__(self, center, image):
        pg.sprite.Sprite.__init__(self)
        self.image = prepare.GFX['other']['bubble']
        if image == 'order':
            inside_image = prepare.GFX['other']['order']
        elif image == 'money':
            inside_image = prepare.GFX['other']['money']
        self.image.blit(inside_image, (0, 0))
        self.rect = self.image.get_rect(center=center)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
