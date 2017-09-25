import pygame as pg
import random

from .. import prepare, tools
from ..components.button import Button
from ..components.label import Label, MultiLineLabel


class MessageScreen(tools._State):
    def __init__(self):
        tools._State.__init__(self)

    def start(self):
        self.image = self.make_image()
        self.rect = self.image.get_rect(
            center=prepare.SCREEN_RECT.center)
        self.labels = self.create_text()
        self.pic = self.create_pic()
        self.buttons = self.create_buttons()

    def make_image(self):
        width = 450
        height = 450
        image = pg.Surface((width, height)).convert()
        image.fill(prepare.FRAME_COLOR)
        image.fill(prepare.FILL_COLOR, rect=pg.rect.Rect(25, 25, 400, 400))
        image.fill(prepare.FRAME_COLOR, rect=pg.rect.Rect(75, 75, 300, 5))
        title_text = self.info_dict['title']
        title = Label(30, title_text, center=(width // 2, 50),
                      font_name='OpenSans-Bold')
        title.draw(image)
        return image

    def create_text(self):
        labels = pg.sprite.Group()
        position = [self.rect.centerx, 225]
        gap = 50
        for text in self.info_dict['text']:
            label = MultiLineLabel(18, text, center=position,
                                   font_name='OpenSans-Regular')
            position[1] += gap
            labels.add(label)

        if self.score_data is not None:
            if self.score_data is False:
                text = 'You have not made it to HS :('
            else:
                text = 'You have made it to HS!!'

            label = MultiLineLabel(18, text, center=position,
                                   font_name='OpenSans-Regular')
            position[1] += gap
            labels.add(label)

        if 'goal' in self.info_dict:
            text = 'GOAL: {}'.format(self.info_dict['goal'])
            goal_label = Label(22, text, center=(self.rect.centerx, 425),
                               font_name='OpenSans-Bold')
            labels.add(goal_label)
        return labels

    def create_pic(self):
        if 'pic' not in self.info_dict:
            return None
        pic_type = self.info_dict['pic']
        if pic_type == 'UFO':
            colors = ('biege', 'blue', 'green', 'pink', 'yellow')
            color = random.choice(colors)
            image = prepare.GFX['ufo']['ufo_{}'.format(color)]
            pic = pg.sprite.Sprite()
            pic.image = image
            center = (self.rect.centerx, 325)
            pic.rect = pic.image.get_rect(center=center)
        return pic

    def create_buttons(self):
        buttons = pg.sprite.Group()
        position = [self.rect.centerx, 485]
        gap = 50
        for button_name in reversed(self.info_dict['buttons']):
            button = Button(20, button_name, self.button_click,
                            center=position, font_name='OpenSans-Bold')
            position[1] -= gap
            buttons.add(button)
        return buttons

    def button_click(self, name):
        if name == 'START':
            self.next = 'GAME'
            self.done = True
        elif name == 'OK':
            if self.info_dict['more_rounds_ahead']:
                self.next = 'GAME'
                self.done = True
            else:
                self.quit = True
        elif name == 'HS':
            self.next = 'HIGH_SCORE'
            self.persist['score_data'] = self.info_dict['score_data']
            self.done = True
        elif name == 'RESTART':
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
            self.info_dict = self.persist['info_dict']
            del self.persist['info_dict']
            if 'score_data' in self.persist:
                self.score_data = self.persist['score_data']
                del self.persist['score_data']
            else:
                self.score_data = None
        screen = pg.display.get_surface()
        screen.blit(self.subscreen, (0, 0))
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

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for label in self.labels:
            label.draw(surface)
        if self.pic is not None:
            surface.blit(self.pic.image, self.pic.rect)
        for button in self.buttons:
            button.draw(surface)

    def update(self, surface, current_time, dt):
        self.draw(surface)
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)
