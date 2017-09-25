import pygame as pg

from .animations import Animation


class Robber(pg.sprite.Sprite):
    def __init__(self, spawn_center, entry, path):
        pg.sprite.Sprite.__init__(self)
        self.image = self.make_image()
        self.rect = self.image.get_rect(center=spawn_center)
        self.speed = 0.4
        self.entry = entry
        self.path = path
        self.start_moving()
        self.mark = None  # marks are created in Waiter

    def make_image(self):
        image = pg.Surface((40, 100)).convert()
        image.fill(pg.Color('brown'))
        return image

    def start_moving(self):
        if self.path:
            self.next_animation()
        else:
            self.path_is_done()

    def next_animation(self):
        if self.path:
            x, y = self.path.pop(0)
            x -= self.rect.width // 2
            y -= self.rect.height // 2
            distance = x - self.rect.x + y - self.rect.y
            distance = (distance ** 2) ** 0.5
            duration = distance // self.speed
            if duration == 0:
                self.path_is_done()
                return
            self.animation = Animation(
                x=x, y=y, duration=duration, round_values=True)
            self.animation.callback = self.next_animation
            self.animation.start(self.rect)
        else:
            self.path_is_done()

    def path_is_done(self):
        self.animation = None

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.mark:
            self.mark.draw(surface)

    def update(self, dt):
        if self.animation:
            self.animation.update(dt * 1000)
