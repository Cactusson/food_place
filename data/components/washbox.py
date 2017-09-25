import pygame as pg

from .. import prepare


class Washbox(pg.sprite.Sprite):
    def __init__(self, center, entry):
        pg.sprite.Sprite.__init__(self)
        self.idle_image = prepare.GFX['other']['washbox']
        # self.idle_image = pg.transform.scale(self.idle_image, (50, 50))
        self.hover_image = prepare.GFX['other']['washbox_hover']
        # self.hover_image = pg.transform.scale(self.hover_image, (50, 50))
        self.image = self.idle_image
        self.rect = self.image.get_rect(center=center)
        self.entry = entry
        self.mark = None  # marks are created in Waiter

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.mark:
            self.mark.draw(surface)

    def update(self, mouse_pos):
        hover = self.rect.collidepoint(mouse_pos)
        if hover:
            self.image = self.hover_image
        else:
            self.image = self.idle_image
