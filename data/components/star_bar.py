import pygame as pg

from .. import prepare, tools


class Star(pg.sprite.Sprite):
    def __init__(self, topleft):
        pg.sprite.Sprite.__init__(self)
        self.image = tools.colorize(prepare.GFX['gui']['star'],
                                    pg.Color('#FFE869'))
        self.rect = self.image.get_rect(topleft=topleft)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class StarBar(pg.sprite.Sprite):
    def __init__(self, topright):
        pg.sprite.Sprite.__init__(self)
        self.image = self.make_image()
        self.rect = self.image.get_rect(topright=topright)
        self.stars = self.make_stars()

    def make_image(self):
        image = pg.Surface((150, 50)).convert()
        image.fill(prepare.FRAME_COLOR)
        return image

    def make_stars(self):
        stars = []
        amount = 3
        topleft = [0, 0]
        gap = 50
        for _ in range(amount):
            star = Star(topleft)
            topleft[0] += gap
            stars.append(star)
        return stars

    def destroy_star(self):
        self.stars.pop()

    def draw(self, surface):
        image = self.image.copy()
        for star in self.stars:
            star.draw(image)
        surface.blit(image, self.rect)
