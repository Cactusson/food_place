import pygame as pg

from .. import prepare, tools
from ..components.button import Button
from ..components.label import Label
from ..components.level_button import LevelButton


class ChooseLevel(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.image = self.make_image()
        self.rect = self.image.get_rect()

    def make_image(self):
        image = pg.Surface(prepare.SCREEN_RECT.size).convert()
        image.fill(prepare.BACKGROUND_COLOR)
        image.fill(prepare.FRAME_COLOR, (200, 100, 600, 150))
        image.fill(prepare.FILL_COLOR, (215, 115, 570, 120))
        image.fill(prepare.FRAME_COLOR, (350, 475, 300, 150))
        image.fill(prepare.FILL_COLOR, (365, 490, 270, 120))
        title = Label(40, 'CHOOSE LEVEL',
                      center=(prepare.SCREEN_RECT.centerx, 50),
                      font_name='OpenSans-Bold')
        title.draw(image)
        return image

    def start(self):
        self.buttons = self.create_buttons()
        self.level_buttons = self.create_level_buttons()
        self.chosen_level_button = None

    def create_buttons(self):
        buttons = pg.sprite.Group()
        play = Button(25, 'PLAY', self.button_click,
                      center=(self.rect.centerx, 525), blocked=True)
        back = Button(25, 'BACK', self.button_click,
                      center=(self.rect.centerx, 575))
        buttons.add(play, back)
        return buttons

    def create_level_buttons(self):
        level_buttons = pg.sprite.Group()
        center = [300, 175]
        gap = 100
        for number in range(5):
            level_button = LevelButton(number + 1, center)
            level_buttons.add(level_button)
            center[0] += gap
        return level_buttons

    def button_click(self, name):
        if name == 'PLAY':
            self.persist['level_number'] = self.chosen_level_button.number
            self.next = 'GAME'
            self.persist['menu_screen'] = pg.display.get_surface().copy()
            self.done = True
        elif name == 'BACK':
            self.next = 'MAIN_MENU'
            self.done = True

    def click_level_button(self):
        for level_button in self.level_buttons:
            if level_button.hover:
                if self.chosen_level_button:
                    self.chosen_level_button.unclick()
                self.chosen_level_button = level_button
                self.chosen_level_button.click()
                for button in self.buttons:
                    if button.name == 'PLAY' and button.blocked:
                        button.unblock()
                break

    def startup(self, persistant):
        self.persist = persistant
        self.start()

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            for button in self.buttons:
                button.click()
            self.click_level_button()

    def draw(self, surface):
        image = self.image.copy()
        for button in self.buttons:
            button.draw(image)
        for level_button in self.level_buttons:
            level_button.draw(image)
        surface.blit(image, self.rect)

    def update(self, surface, current_time, dt):
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)
        self.level_buttons.update(mouse_pos)
        self.draw(surface)
