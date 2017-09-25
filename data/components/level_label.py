import pygame as pg

from .label import Label


class LevelLabel(pg.sprite.Sprite):
    def __init__(self, number, center):
        pg.sprite.Sprite.__init__(self)
        self.image = self.make_image(number)
        self.rect = self.image.get_rect(center=center)

    def make_image(self, number):
        size = 40
        image = pg.Surface((size, size)).convert()
        image.set_alpha(0)
        image = image.convert_alpha()
        pg.draw.circle(
            image, pg.Color('#EDF2F6'), (size // 2, size // 2), size // 2)
        label = Label(20, str(number), center=(size // 2, size // 2),
                      font_name='OpenSans-Bold')
        label.draw(image)
        return image

    def draw(self, surface):
        surface.blit(self.image, self.rect)
