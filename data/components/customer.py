# import itertools
import pygame as pg
import random

from .. import prepare
from .task import Task


class Customer(pg.sprite.Sprite):
    image_dict = {
        'red': {
            'idle': prepare.GFX['customers_simple']['customer_red'],
            'hover': prepare.GFX['customers_simple']['customer_red_hover'],
        },
        'blue': {
            'idle': prepare.GFX['customers_simple']['customer_blue'],
            'hover': prepare.GFX['customers_simple']['customer_blue_hover'],
        }
    }

    def __init__(self, color):
        pg.sprite.Sprite.__init__(self)
        # self.idle_image = prepare.GFX['customers_new']['customer']
        # self.hover_image = prepare.GFX['customers_new']['customer_hover']
        # self.images_walking = itertools.cycle([
        #     prepare.GFX['customers_new']['customer_walking_{}'.format(i)]
        #     for i in range(1, 3)] + [self.idle_image] +
        #     [prepare.GFX['customers_new']['customer_walking_{}'.format(i)]
        #         for i in range(3, 5)] + [self.idle_image])
        # self.images_hand_up = [
        #     prepare.GFX['customers']['customer{}'.format(i)]
        #     for i in range(1, 4)]
        # self.images_hand_down = [
        #     prepare.GFX['customers']['customer{}'.format(
        #         i)] for i in range(3, 0, -1)]
        # self.images_itch = [prepare.GFX['customers']['customer{}'.format(i)]
        #                     for i in range(4, 7)]
        # self.image = self.idle_image
        self.color = color
        empty_image = pg.Surface((40, 40)).convert()
        empty_image.set_alpha(0)
        empty_image = empty_image.convert_alpha()
        self.idle_image = empty_image.copy()
        pg.draw.circle(self.idle_image, pg.Color(self.color), (20, 20), 20)
        pg.draw.circle(self.idle_image, pg.Color('black'), (20, 20), 20, 4)
        self.hover_image = empty_image.copy()
        pg.draw.circle(self.hover_image, pg.Color(self.color), (20, 20), 20)
        pg.draw.circle(
            self.hover_image, pg.Color('lightgray'), (20, 20), 20, 4)
        # self.idle_image = self.image_dict[self.color]['idle']
        # self.hover_image = self.image_dict[self.color]['hover']
        self.image = self.idle_image
        self.rect = self.image.get_rect()
        self.idle = False
        self.animate = False
        self.animation_routine = None
        self.image_index = 0
        self.tasks = pg.sprite.Group()

    def update_image_entry(self, frame):
        if frame != 0:
            return

        self.image = next(self.images_walking)

    def start_animation_timer(self):
        until_animation = random.randint(1, 2) * 1000
        self.timer_task = Task(self.start_animation, until_animation)
        self.tasks.add(self.timer_task)

    def start_animation(self):
        self.stop_animation_timer()
        if self.animate:
            self.stop_animation()
        if self.idle:
            self.animate = True
            self.animation_routine = 'HAND_UP'
            self.image_index = 0

    def stop_animation_timer(self):
        self.timer_task.kill()

    def stop_animation(self):
        # self.image = self.idle_image
        self.animate = False
        self.tasks.empty()
        self.animation_routine = None
        if self.idle:
            self.start_animation_timer()

    def animation_stop_itching(self):
        self.animation_routine = 'HAND_DOWN'
        self.image_index = 0

    def lock_hover_image(self):
        if self.animate:
            pass
            # self.stop_animation()
        # self.stop_animation_timer()
        self.image = self.hover_image

    def unlock_hover_image(self):
        self.image = self.idle_image
        # if self.idle:
        #     self.start_animation_timer()

    def entry_is_done(self):
        self.idle = True
        # self.start_animation_timer()
        # self.image = self.idle_image

    def hover(self):
        self.image = self.hover_image

    def unhover(self):
        self.image = self.idle_image

    def update_image_animate(self, frame):
        if frame != 0:
            return

        if self.animation_routine:
            if self.animation_routine == 'HAND_UP':
                self.image = self.images_hand_up[self.image_index]
                self.image_index += 1
                if self.image_index >= len(self.images_hand_up):
                    self.image_index = 0
                    self.animation_routine = 'ITCHING'
                    task = Task(self.animation_stop_itching, 2000)
                    self.tasks.add(task)
            elif self.animation_routine == 'ITCHING':
                self.image = self.images_itch[self.image_index]
                self.image_index += 1
                if self.image_index >= len(self.images_itch):
                    self.image_index = 0
            elif self.animation_routine == 'HAND_DOWN':
                self.image = self.images_hand_down[self.image_index]
                self.image_index += 1
                if self.image_index >= len(self.images_hand_down):
                    self.stop_animation()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, dt, frame, entry_update):
        self.tasks.update(dt * 1000)
        # if entry_update:
        #     self.update_image_entry(frame)
        # if self.animate:
        #     self.update_image_animate(frame)
