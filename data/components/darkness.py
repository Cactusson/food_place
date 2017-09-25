import pygame as pg

from .. import prepare
from .task import Task


class Darkness(pg.sprite.Sprite):
    def __init__(self, callback_closed, callback_opened):
        pg.sprite.Sprite.__init__(self)
        self.callback_closed = callback_closed
        self.callback_opened = callback_opened
        self.tasks = pg.sprite.Group()
        self.max_vision = (1500, 1500)
        self.min_vision = (1, 1)
        self.change_rate = (20, 20)
        self.vision_rect = pg.rect.Rect((0, 0), self.max_vision)
        self.state = 'IDLE'
        self.empty_cover = pg.Surface(prepare.SCREEN_SIZE).convert_alpha()
        self.empty_cover.fill((0, 0, 0))

    def make_image(self, center):
        cover = self.empty_cover.copy()
        self.vision_rect.center = center
        pg.draw.circle(cover, (0, 0, 0, 0), self.vision_rect.center,
                       self.vision_rect.width // 2)
        return cover

    def start_shrinking(self):
        self.state = 'SHRINKING'
        self.tasks.empty()
        task = Task(self.shrink, 5, -1)
        self.tasks.add(task)

    def shrink(self):
        self.vision_rect.width -= self.change_rate[0]
        self.vision_rect.height -= self.change_rate[1]
        if (self.vision_rect.width <= self.min_vision[0] or
                self.vision_rect.height <= self.min_vision[1]):
            self.vision_rect.size = self.min_vision
            self.stop_shrinking()

    def stop_shrinking(self):
        self.tasks.empty()
        self.callback_closed()
        self.start_growing()

    def start_growing(self):
        self.tasks.empty()
        task = Task(self.grow, 5, -1)
        self.tasks.add(task)

    def grow(self):
        self.vision_rect.width += self.change_rate[0]
        self.vision_rect.height += self.change_rate[1]
        if (self.vision_rect.width >= self.max_vision[0] or
                self.vision_rect.height >= self.max_vision[1]):
            self.vision_rect.size = self.max_vision
            self.stop_growing()

    def stop_growing(self):
        self.tasks.empty()
        self.callback_opened()

    def draw(self, surface):
        surface.blit(self.image, (0, 0))

    def update(self, center, dt):
        self.image = self.make_image(center)
        self.tasks.update(dt * 1000)
