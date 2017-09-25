import pygame as pg

from .. import prepare
from .task import Task


class Laser(pg.sprite.Sprite):
    """
    Laser is just a visual effect, that appears when a ufo starts to ascend.
    It fades shortly after ufo is gone.
    After that the passed callback is called.
    """
    def __init__(self, color, midbottom, callback):
        pg.sprite.Sprite.__init__(self)
        self.tasks = pg.sprite.Group()
        self.color = color
        image = prepare.GFX['ufo']['laser_ground_{}'.format(self.color)].copy()
        rect = image.get_rect(midbottom=midbottom)
        self.sprites = [(image, rect)]
        self.callback = callback
        self.alpha = 255
        self.alpha_step = 20

    def grow(self, midbottom):
        image = prepare.GFX['ufo']['laser_{}'.format(self.color)].copy()
        rect = image.get_rect(midbottom=midbottom)
        self.sprites.append((image, rect))

    def start_fading(self):
        task = Task(self.fade, 100, -1)
        self.tasks.add(task)

    def fade(self):
        self.alpha = max(self.alpha - self.alpha_step, 0)
        if self.alpha == 0:
            self.finish_fading()
            return
        for image, _ in self.sprites:
            image.fill((255, 255, 255, self.alpha),
                       special_flags=pg.BLEND_RGBA_MULT)

    def finish_fading(self):
        self.tasks.empty()
        self.callback()

    def draw(self, surface):
        for image, rect in reversed(self.sprites):
            surface.blit(image, rect)

    def update(self, dt):
        self.tasks.update(dt * 1000)
