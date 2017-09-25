import pygame as pg

from .. import prepare
from .animations import Animation


class Firearm(pg.sprite.Sprite):
    def __init__(self, center, entry):
        pg.sprite.Sprite.__init__(self)
        image = pg.transform.scale(prepare.GFX['rifle']['rifle'], (112, 105))
        self.image = pg.transform.rotate(image, 90)
        target_rect = self.image.get_rect(center=center)
        self.rect = target_rect.move(0, -100)
        animation = Animation(
            x=target_rect.x, y=target_rect.y, duration=500,
            round_values=True)
        animation.start(self.rect)
        self.animations = pg.sprite.Group(animation)
        self.entry = entry
        self.state = 'READY'
        self.mark = None  # marks are created in Waiter

    def empty(self):
        self.state = 'EMPTY'

    def load(self):
        self.state = 'READY'

    def disappear(self, callback):
        end_rect = self.rect.move(0, -100)
        animation = Animation(
            x=end_rect.x, y=end_rect.y, duration=500,
            round_values=True)
        animation.callback = callback
        animation.start(self.rect)
        self.animations = pg.sprite.Group(animation)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.mark:
            self.mark.draw(surface)

    def update(self, dt):
        self.animations.update(dt * 1000)


class Rifle(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.idle_image = pg.transform.scale(prepare.GFX['rifle']['rifle'],
                                             (112, 105))
        self.fire_images = [pg.transform.scale(prepare.GFX['rifle'][
            'rifle_fire_{}'.format(i)], (112, 105)) for i in range(1, 9)]
        self.fire_images.extend(self.fire_images[6:4:-1])
        self.image = self.idle_image
        self.rect = self.image.get_rect(center=center)
        self.shooting = False
        self.image_index = 0

    def start_shooting(self):
        self.shooting = True

    def stop_shooting(self):
        self.image = self.idle_image
        self.image_index = 0
        self.shooting = False

    def update_image(self, frame):
        if frame != 0:
            return

        if self.image_index >= len(self.fire_images):
            self.stop_shooting()
            return
        self.image = self.fire_images[self.image_index]
        self.image_index += 1

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, frame):
        if self.shooting:
            self.update_image(frame)
