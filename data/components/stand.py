import pygame as pg

from .. import prepare
from .meal import Meal


class Stand(pg.sprite.Sprite):
    def __init__(self, center, meal_1_entry, meal_2_entry):
        pg.sprite.Sprite.__init__(self)
        self.image = prepare.GFX['other']['stand']
        self.rect = self.image.get_rect(center=center)
        self.meal_1_entry = meal_1_entry
        self.meal_2_entry = meal_2_entry
        self.places = [None, None, None, None]

    def make_image(self):
        image = pg.Surface((300, 80)).convert()
        image.fill(pg.Color('brown'))
        return image

    def able_to_add_meal(self):
        for place in self.places:
            if place is None:
                return True
        return False

    def add_meal(self, number):
        for indx in range(len(self.places)):
            if self.places[indx] is None:
                place = indx
                break
        else:
            print('Something went wrong with stand.')
            return

        center = self.rect.left + 125 + 65 * place, self.rect.centery - 50
        if place == 0 or place == 1:
            entry = self.meal_1_entry
        else:
            entry = self.meal_2_entry

        meal = Meal(center, entry, number)
        self.places[place] = meal
        return meal

    def clear_meal(self, meal):
        for indx in range(len(self.places)):
            if self.places[indx] == meal:
                self.places[indx] = None

    def draw(self, surface):
        surface.blit(self.image, self.rect)
