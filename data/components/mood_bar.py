import pygame as pg


class MoodBar(pg.sprite.Sprite):
    def __init__(self, center, mood=5):
        pg.sprite.Sprite.__init__(self)
        self.size = 10
        self.colors = [pg.Color('red'), pg.Color('pink'), pg.Color('yellow'),
                       pg.Color('lightgreen'), pg.Color('green')]
        self.empty_image = self.make_empty_image()
        self.update_image(mood)
        self.rect = self.image.get_rect(center=center)

    def make_empty_image(self):
        image = pg.Surface((self.size * 5, self.size)).convert()
        # image.set_alpha(0)
        # image = image.convert_alpha()
        image.fill(pg.Color('black'))
        return image

    def update_image(self, mood):
        self.image = self.empty_image.copy()
        for x in range(mood):
            center = x * self.size + self.size // 2, self.size // 2
            pg.draw.circle(
                self.image, self.colors[mood - 1], center, self.size // 2)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
