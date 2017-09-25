import pygame as pg

from .. import prepare
from .task import Task


class Timer(pg.sprite.Sprite):
    def __init__(self, mode, time=None, callback=None, topleft=(60, 0)):
        """
        Timer can be either 'STOPWATCH' or 'COUNTDOWN'.
        Attributes 'time' and 'callback' are needed for the last one.
        """
        pg.sprite.Sprite.__init__(self)
        self.tasks = pg.sprite.Group()
        character_size = (55, 55)
        self.images = [pg.transform.scale(prepare.GFX['numbers'][
            'num_{}'.format(i)], character_size) for i in range(10)]
        self.images.append(pg.transform.scale(
            prepare.GFX['numbers']['colon'], character_size))

        self.empty_image = self.make_empty_image()
        self.rect = self.empty_image.get_rect(topleft=topleft)

        self.mode = mode
        if self.mode == 'STOPWATCH':
            self.current_time = 0
        elif self.mode == 'COUNTDOWN':
            self.current_time = self.time_from_text(time)
            self.callback = callback

        self.update_image()
        self.on = False

    def make_empty_image(self):
        empty_image = pg.Surface((150, 50)).convert()
        empty_image.set_alpha(0)
        empty_image = empty_image.convert_alpha()
        # empty_image.fill(pg.Color('lightblue'))
        return empty_image

    def update_image(self):
        self.image = self.empty_image.copy()
        text = self.time_to_text()
        gap = 25
        for i, ch in enumerate(text):
            if ch == ':':
                indx = 10
            else:
                indx = int(ch)
            self.image.blit(self.images[indx], (gap * i - gap // 2, 0))

    def time_to_text(self):
        minutes = str(self.current_time // 60)
        if len(minutes) == 1:
            minutes = '0' + minutes
        seconds = str(self.current_time % 60)
        if len(seconds) == 1:
            seconds = '0' + seconds
        return '{}:{}'.format(minutes, seconds)

    def time_from_text(self, time):
        minutes, seconds = map(int, time.split(':'))
        return minutes * 60 + seconds

    def start(self):
        self.on = True
        task = Task(self.next_second, 1000)
        self.tasks.add(task)

    def finish(self):
        self.on = False
        self.callback()

    def next_second(self):
        self.current_time += (1 if self.mode == 'STOPWATCH' else -1)
        self.update_image()
        if self.mode == 'COUNTDOWN' and self.current_time == 0:
            self.finish()
            return
        task = Task(self.next_second, 1000)
        self.tasks.add(task)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, dt):
        if self.on:
            self.tasks.update(dt * 1000)
