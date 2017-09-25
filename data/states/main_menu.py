import pygame as pg

from .. import prepare, tools

from ..components.label import Label
from ..components.menu_button_system import MenuButtonSystem


class MainMenu(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        center = prepare.SCREEN_RECT.center[0], 85
        self.title = Label(45, 'FOOD PLACE', center=center,
                           font_name='OpenSans-Bold')
        center = (prepare.SCREEN_RECT.center[0],
                  prepare.SCREEN_RECT.center[1] + 50)
        self.button_system = MenuButtonSystem(center, self.move_on)

    def move_on(self, command):
        if command == 'FINITE':
            self.next = 'CHOOSE_LEVEL'
        elif command == 'INFINITE':
            self.next = 'GAME'
            self.persist['menu_screen'] = pg.display.get_surface().copy()
        elif command == 'HIGH_SCORE':
            self.next = 'HIGH_SCORE'
        elif command == 'QUIT':
            self.quit = True
        self.done = True

    def startup(self, persistant):
        self.persist = persistant

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.button_system.button_click()

    def draw(self, surface):
        surface.fill(prepare.BACKGROUND_COLOR)
        self.title.draw(surface)
        self.button_system.draw(surface)

    def update(self, surface, current_time, dt):
        mouse_pos = pg.mouse.get_pos()
        self.button_system.update(mouse_pos)
        self.draw(surface)
