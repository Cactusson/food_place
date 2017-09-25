import pygame as pg

from .. import prepare, tools

from ..components.button import Button
from ..components.hstable import HSTable
from ..components.label import Label


class HighScore(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.image = self.make_image()
        self.rect = self.image.get_rect()
        self.buttons = self.make_buttons()

    def start(self):
        """
        This function runs every time, the game goes in this state.
        """
        self.hstable = HSTable()
        self.hstable.load_table()
        self.hstable.create_big_image((prepare.SCREEN_RECT.centerx, 275),
                                      self.score_data)

    def make_image(self):
        image = pg.Surface(prepare.SCREEN_RECT.size).convert()
        image.fill(prepare.BACKGROUND_COLOR)
        image.fill(prepare.FRAME_COLOR, (200, 100, 600, 350))
        image.fill(prepare.FILL_COLOR, (215, 115, 570, 320))
        image.fill(prepare.FRAME_COLOR, (350, 475, 300, 150))
        image.fill(prepare.FILL_COLOR, (365, 490, 270, 120))
        title = Label(45, 'HIGH SCORE',
                      center=(prepare.SCREEN_RECT.center[0], 50),
                      font_name='OpenSans-Bold')
        title.draw(image)
        return image

    def make_buttons(self):
        buttons = pg.sprite.Group()
        names = ('CLEAR', 'BACK')
        center = (self.rect.width // 2, 525)
        gap = 50
        centers = [(center[0], center[1] + gap * i) for i in range(len(names))]
        for name, center in zip(names, centers):
            button = Button(22, name, self.button_press, center=center,
                            font_name='OpenSans-Bold')
            buttons.add(button)
        return buttons

    def button_press(self, name):
        if name == 'CLEAR':
            print('This shit is not implemented yet.')
        elif name == 'BACK':
            self.done = True

    def startup(self, persistant):
        self.persist = persistant
        if self.previous == 'MAIN_MENU':
            self.next = 'MAIN_MENU'
            self.score_data = None
        elif self.previous == 'MESSAGE_SCREEN':
            self.next = 'MESSAGE_SCREEN'
            if 'score_data' in self.persist:
                self.score_data = self.persist['score_data']
                del self.persist['score_data']
        self.start()

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in self.buttons:
                    button.click()

    def draw(self, surface):
        image = self.image.copy()
        for button in self.buttons:
            button.draw(image)
        self.hstable.draw(image)
        surface.blit(image, self.rect)

    def update(self, surface, current_time, dt):
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)
        self.draw(surface)
