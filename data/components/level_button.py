import pygame as pg

from .label import Label


class LevelButton(pg.sprite.Sprite):
    def __init__(self, number, center):
        pg.sprite.Sprite.__init__(self)
        self.number = number
        self.idle_image, self.hover_image, self.clicked_image = \
            self.make_images()
        self.image = self.idle_image
        self.rect = self.image.get_rect(center=center)
        self.hover = False
        self.clicked = False

    def make_images(self):
        size = 70
        image = pg.Surface((size, size)).convert()
        image.set_alpha(0)
        image = image.convert_alpha()
        idle_color = pg.Color('#FCF0C8')
        idle_text_color = pg.Color('black')
        hover_color = pg.Color('#B51A62')
        clicked_color = pg.Color('#91E4A6')
        clicked_text_color = pg.Color('white')
        center = (size // 2, size // 2)
        radius = size // 2
        width = 5

        idle_image = image.copy()
        pg.draw.circle(idle_image, idle_color, center, radius - width)
        idle_label = Label(25, str(self.number), color=idle_text_color,
                           center=center, font_name='OpenSans-Regular')
        idle_label.draw(idle_image)

        hover_image = image.copy()
        pg.draw.circle(hover_image, hover_color, center, radius)
        pg.draw.circle(hover_image, idle_color, center, radius - width)
        hover_label = Label(25, str(self.number), color=idle_text_color,
                            center=center, font_name='OpenSans-Regular')
        hover_label.draw(hover_image)

        clicked_image = image.copy()
        pg.draw.circle(clicked_image, clicked_color, center, radius - width)
        clicked_label = Label(25, str(self.number), color=clicked_text_color,
                              center=center, font_name='OpenSans-Regular')
        clicked_label.draw(clicked_image)

        return idle_image, hover_image, clicked_image

    def click(self):
        self.clicked = True
        self.hover = False
        self.image = self.clicked_image

    def unclick(self):
        self.clicked = False
        self.image = self.idle_image

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, mouse_pos):
        if self.clicked:
            return
        hover = self.rect.collidepoint(mouse_pos)
        if hover:
            self.image = self.hover_image
        else:
            self.image = self.idle_image
        self.hover = hover
