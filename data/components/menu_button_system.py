import pygame as pg

from .. import prepare
from .button import Button


class MenuButtonSystem(pg.sprite.Sprite):
    def __init__(self, center, callback):
        self.image = self.make_image()
        self.rect = self.image.get_rect(center=center)
        self.buttons = self.make_buttons()
        self.callback = callback

    def make_image(self):
        image = pg.Surface((400, 400)).convert()
        image.fill(prepare.FRAME_COLOR)
        image.fill(prepare.FILL_COLOR, (25, 25, 350, 350))
        return image

    def make_buttons(self):
        buttons = pg.sprite.Group()
        center = [self.rect.width // 2, 75]
        gap = 75
        names = ('PLAY', 'INFINITE MODE', 'HIGH SCORE', 'QUIT')
        for name in names:
            button = Button(
                25, name, self.button_press, center=center,
                font_name='OpenSans-Bold')
            buttons.add(button)
            button.collide_rect = button.rect.move(*self.rect.topleft)
            center[1] += gap
        return buttons

    def button_press(self, button_name):
        if button_name == 'PLAY':
            button_result = 'FINITE'
        elif button_name == 'INFINITE MODE':
            button_result = 'INFINITE'
        elif button_name == 'HIGH SCORE':
            button_result = 'HIGH_SCORE'
        elif button_name == 'QUIT':
            button_result = 'QUIT'
        self.callback(button_result)

    def button_click(self):
        for button in self.buttons:
            button.click()

    def draw(self, surface):
        image = self.image.copy()
        for button in self.buttons:
            button.draw(image)
        surface.blit(image, self.rect)

    def update(self, mouse_pos):
        for button in self.buttons:
            button.update(mouse_pos)
