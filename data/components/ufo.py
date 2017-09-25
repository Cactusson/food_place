import pygame as pg
import random

from .. import prepare

from .animations import Animation
from .bubble import Bubble
from .flag import Flag
from .label import Label
from .laser import Laser
from .order import Order


class UFO(pg.sprite.Sprite):
    colors = ('biege', 'blue', 'green', 'pink', 'yellow')

    def __init__(self, center, entry, number=0):
        pg.sprite.Sprite.__init__(self)
        self.number = number
        self.color = random.choice(self.colors)
        self.image = prepare.GFX['ufo']['ufo_{}'.format(self.color)]
        self.rect = self.image.get_rect(center=center)
        self.entry = entry
        self.flag = Flag(self.number, self.rect)
        self.animations = pg.sprite.Group()
        self.bubble_center = self.rect.centerx, self.rect.top - 50
        self.bubble = None
        self.label = None
        self.laser = None
        self.change_state('FLYING')
        self.mark = None  # marks are created in Waiter

    def change_state(self, new_state):
        self.state = new_state
        if self.state == 'FLYING':
            if self.label:
                self.label = None
            if self.bubble:
                self.bubble = None
        if self.state == 'READY_TO_ORDER':
            self.bubble = Bubble(self.bubble_center, 'order')
            self.update_label()
        elif self.state == 'WAITING':
            self.bubble = None
            self.update_label()

    def produce_order(self):
        order = Order(self.number)
        return order

    def update_label(self):
        center = self.rect.centerx, self.rect.top - 15
        self.label = Label(25, self.state, center=center, bg=pg.Color('white'))

    def arrive(self, callback):
        x, y = self.rect.topleft
        self.rect.bottom = 0
        animation = Animation(
            x=x, y=y, duration=1000, round_values=True, transition='in_quint')
        animation.callback = callback
        animation.start(self.rect)
        self.animations.add(animation)

    def depart(self, callback):
        self.create_laser(callback)
        self.change_state('FLYING')
        x, y = self.rect.x, -self.rect.height
        animation = Animation(
            x=x, y=y, duration=1000, round_values=True, transition='in_quad')
        animation.callback = self.fade_laser
        animation.update_callback = self.grow_laser
        self.next_midbottom = self.rect.midbottom
        animation.start(self.rect)
        self.animations.add(animation)

    def create_laser(self, callback):
        self.laser = Laser(self.color, self.rect.midbottom, callback)

    def grow_laser(self):
        if self.rect.midbottom[1] <= self.next_midbottom[1]:
            self.laser.grow(self.next_midbottom)
            self.next_midbottom = (self.next_midbottom[0],
                                   self.next_midbottom[1] - 100)

    def fade_laser(self):
        self.laser.start_fading()

    def draw(self, surface):
        if self.laser:
            self.laser.draw(surface)
        surface.blit(self.image, self.rect)
        if self.label:
            self.label.draw(surface)
        if self.state == 'WAITING':
            self.flag.draw(surface)
        if self.bubble:
            self.bubble.draw(surface)
        if self.mark:
            self.mark.draw(surface)

    def update(self, dt):
        self.animations.update(dt * 1000)
        if self.laser:
            self.laser.update(dt)
