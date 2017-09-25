import pygame as pg

from .. import prepare, tools
from ..components.button import Button
from ..components.label import Label


class Pause(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.cover = self.make_cover_image()
        self.basic_image = self.make_image()
        self.rect = self.basic_image.get_rect(
            center=prepare.SCREEN_RECT.center)
        self.image = self.basic_image.copy()
        self.buttons = self.make_buttons()

    def make_image(self):
        width = 450
        height = 450
        image = pg.Surface((width, height)).convert()
        image.fill(prepare.FRAME_COLOR)
        image.fill(prepare.FILL_COLOR, rect=pg.rect.Rect(25, 25, 400, 400))
        title = Label(30, 'PAUSE', center=(width // 2, 50),
                      font_name='OpenSans-Bold')
        title.draw(image)
        return image

    def make_cover_image(self):
        cover = pg.Surface(prepare.SCREEN_SIZE).convert()
        cover.set_alpha(200)
        return cover

    def make_buttons(self):
        """
        There are three buttons in the menu, each has its own call function.
        (their names start with 'button_')
        """
        buttons = pg.sprite.Group()
        play = Button(
            25, 'PLAY', self.button_click, center=(self.rect.centerx, 250),
            font_name='OpenSans-Bold')
        quit = Button(
            25, 'QUIT', self.button_click, center=(self.rect.centerx, 375),
            font_name='OpenSans-Bold')
        buttons.add(play, quit)
        return buttons

    def button_click(self, name):
        if name == 'PLAY':
            self.next = 'GAME'
            self.done = True
        elif name == 'QUIT':
            self.next = 'MAIN_MENU'
            self.done = True

    def startup(self, persistant):
        self.persist = persistant
        if self.previous == 'GAME':
            self.subscreen = self.persist['screen']
            del self.persist['screen']
        screen = pg.display.get_surface()
        screen.blit(self.subscreen, (0, 0))
        screen.blit(self.cover, (0, 0))

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
            elif event.key == pg.K_q:
                self.next = 'GAME'
                self.done = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            for button in self.buttons:
                button.click()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for button in self.buttons:
            button.draw(surface)

    def update(self, surface, current_time, dt):
        self.draw(surface)
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)
