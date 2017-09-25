import pygame as pg

from .. import prepare
from .label import Label, FlyingLabel


class Seat(pg.sprite.Sprite):
    """
    Seat is a part of a table. It can be occupied by a customer
    or be empty. It can have color and color bonuses.
    """
    images_dict = {
        'none': prepare.GFX['table_simple']['seat_gray'],
        'red': prepare.GFX['table_simple']['seat_red'],
        'blue': prepare.GFX['table_simple']['seat_blue'],
        'green': prepare.GFX['table_simple']['seat_green']
    }

    def __init__(self, topleft, color):
        pg.sprite.Sprite.__init__(self)
        self.color = color
        self.image = self.images_dict[self.color]
        self.rect = self.image.get_rect(topleft=topleft)
        self.customer = None
        self.color_bonus = None
        self.color_multiplier = 1
        self.color_multiplier_label = None
        self.flying_labels = pg.sprite.Group()
        self.flying_labels_offsets = (-20, -45)

    def get_customer(self, customer):
        self.customer = customer
        self.customer.rect.center = self.rect.center
        if self.customer.color == self.color:
            self.color_bonus = 100

    def sit_customer(self):
        if self.color != self.customer.color:
            self.color = self.customer.color
            self.image = self.images_dict[self.color]
            self.color_multiplier = 1
            self.color_multiplier_label = None
        # if self.customer:
        #     self.customer.state = 'SIT'

    def empty(self):
        self.customer = None
        self.color_bonus = None

    def grow_color_multiplier(self):
        self.color_multiplier += 1
        text = 'x{}'.format(self.color_multiplier)
        self.color_multiplier_label = Label(25, text, center=self.rect.center)

    def create_flying_label(self, points):
        text = 'COLOR x{}'.format(self.color_multiplier)
        center = (
            self.rect.centerx, self.rect.top + self.flying_labels_offsets[1])
        label_color = FlyingLabel(28, text, center=center, color=self.color)
        self.flying_labels.add(label_color)
        text = '+{}'.format(points)
        center = (
            self.rect.centerx, self.rect.top + self.flying_labels_offsets[0])
        label_points = FlyingLabel(28, text, center=center, color=self.color)
        self.flying_labels.add(label_points)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.color_multiplier_label:
            self.color_multiplier_label.draw(surface)
        if self.customer:
            self.customer.draw(surface)
        for label in self.flying_labels:
            label.draw(surface)

    def update(self, dt):
        for label in self.flying_labels:
            label.update(dt)
