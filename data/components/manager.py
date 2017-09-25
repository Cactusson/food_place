import pygame as pg
import random

from .task import Task


class Manager:
    def __init__(self, mode, data, game_events):
        self.mode = mode
        self.data = data
        self.game_events = game_events
        self.tasks = pg.sprite.Group()
        if self.mode == 'FINITE':
            self.customers_data = list(self.data['customers'])
            if 'ufo' in self.data:
                self.ufo_intervals = list(self.data['ufo'])
            else:
                self.ufo_intervals = None
            if 'robber' in self.data:
                self.robber_intervals = list(self.data['robber'])
            else:
                self.robber_intervals = None
            if self.ufo_intervals is not None:
                self.create_ufo_task()
            if self.robber_intervals is not None:
                self.create_robber_task()
        elif self.mode == 'INFINITE':
            self.create_ufo_task()
            self.create_robber_task()

        self.create_customer_task()

    def create_customer_task(self):
        if self.mode == 'FINITE':
            if not self.customers_data:
                return
            interval, self.customer_colors = self.customers_data.pop(0)
        elif self.mode == 'INFINITE':
            interval = random.randint(10, 20) * 1000
            amount = random.randint(1, 4)
            colors = ('red', 'blue', 'green')
            self.customer_colors = [
                random.choice(colors) for _ in range(amount)]
        task = Task(self.create_customer, interval)
        self.tasks.add(task)

    def customer_short_interval(self):
        interval = 5000
        task = Task(self.create_customer, interval)
        self.tasks.add(task)

    def create_customer(self):
        self.game_events.append(('ADD CUSTOMER', self.customer_colors))

    def create_ufo_task(self):
        if self.mode == 'FINITE':
            if not self.ufo_intervals:
                return
            interval = self.ufo_intervals.pop(0)
        elif self.mode == 'INFINITE':
            interval = 25000
        task = Task(self.create_ufo, interval)
        self.tasks.add(task)

    def ufo_short_interval(self):
        interval = 5000
        task = Task(self.create_ufo, interval)
        self.tasks.add(task)

    def create_ufo(self):
        self.game_events.append(('ADD UFO',))

    def create_robber_task(self):
        if self.mode == 'FINITE':
            if not self.robber_intervals:
                return
            interval = self.robber_intervals.pop(0)
        elif self.mode == 'INFINITE':
            interval = 25000
        task = Task(self.create_robber, interval)
        self.tasks.add(task)

    def robber_short_interval(self):
        interval = 5000
        task = Task(self.create_robber, interval)
        self.tasks.add(task)

    def create_robber(self):
        self.game_events.append(('ADD ROBBER',))

    def update(self, dt):
        self.tasks.update(dt * 1000)
