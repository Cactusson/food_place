import pygame as pg


class Dish(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = self.make_image()
        self.rect = self.image.get_rect()

    def __str__(self):
        return "DIRTY DISHES"

    def make_image(self):
        size = 25
        image = pg.Surface((size, size)).convert()
        image.fill(pg.Color('brown'))
        return image

    def draw(self, surface):
        surface.blit(self.image, self.rect)
