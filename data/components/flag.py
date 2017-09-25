import pygame as pg

from .label import Label


class Flag(pg.sprite.Sprite):
    def __init__(self, number, rect):
        pg.sprite.Sprite.__init__(self)
        self.number = number
        self.idle_image, self.fired_image = self.make_images()
        self.image = self.idle_image
        self.rect = self.image.get_rect(center=rect.center)

    def make_images(self):
        size = 25
        idle_color = pg.Color('white')
        fired_color = pg.Color('orange')
        label = Label(20, str(self.number), center=(size // 2, size // 2))
        image = pg.Surface((size, size)).convert()
        idle_image = image.copy()
        idle_image.fill(idle_color)
        idle_image.blit(label.image, label.rect)
        fired_image = image.copy()
        fired_image.fill(fired_color)
        fired_image.blit(label.image, label.rect)
        return idle_image, fired_image

    def fire_up(self):
        self.image = self.fired_image

    def back_to_normal(self):
        self.image = self.idle_image

    def draw(self, surface):
        surface.blit(self.image, self.rect)
