import pygame as pg
import random

from .animations import Animation
from .customer import Customer
from .mood_bar import MoodBar
from .task import Task


class CustomerGroup(pg.sprite.Sprite):
    def __init__(self, colors, end_topright, topright):
        pg.sprite.Sprite.__init__(self)
        self.animations = pg.sprite.Group()
        self.tasks = pg.sprite.Group()
        self.amount = len(colors)
        self.customers = self.create_customers(colors)
        self.rect = self.create_rect(topright)
        self.place_customers()
        self.queue_rect = self.rect.copy()
        self.queue_rect.topright = end_topright
        self.hovered = False
        self.entering = False
        self.state = 'IDLE'
        self.clicked_offset = [0, 0]
        self.original_rect = self.rect.copy()
        self.return_speed = 1.3
        self.entry_speed = 0.4
        self.show = True
        self.mood = 5
        self.mood_bar = MoodBar((self.rect.centerx, self.rect.top - 15))
        self.mood_change_time = (9000, 11000)
        self.to_move_down = False
        self.pause_time = None

    def start(self):
        self.entering = True
        self.create_entry_animation()
        time = random.randint(*self.mood_change_time)
        task = Task(self.decrease_mood, time)
        self.tasks.add(task)

    def create_customers(self, colors):
        customers = pg.sprite.Group()
        for color in colors:
            customer = Customer(color)
            customers.add(customer)
        return customers

    def create_rect(self, topright):
        width = self.customers.sprites()[0].rect.width * self.amount
        height = self.customers.sprites()[0].rect.height
        rect = pg.rect.Rect((0, 0), (width, height))
        rect.topright = topright
        return rect

    def place_customers(self):
        for indx, customer in enumerate(self.customers):
            customer.rect.topleft = (
                self.rect.x + indx * customer.rect.width, self.rect.y)

    def create_entry_animation(self):
        point = self.queue_rect.topleft
        distance = point[1] - self.rect.y
        duration = distance // self.entry_speed
        if duration == 0:
            self.entry_is_done()
            return
        animation = Animation(
            x=point[0], y=point[1], duration=duration, round_values=True)
        animation.callback = self.entry_is_done
        animation.start(self.rect)
        self.animations.add(animation)

    def pause_entry_animation(self):
        self.pause_time = pg.time.get_ticks()

    def entry_is_done(self):
        if self.rect.center == self.queue_rect.center:
            self.entering = False
            self.state = 'IDLE'
            for customer in self.customers:
                customer.entry_is_done()
        else:
            self.create_entry_animation()

    def click(self, mouse_pos):
        if self.state in ('CLICK', 'RETURN'):
            return
        self.state = 'CLICK'
        self.show = True
        if self.entering:
            self.pause_entry_animation()
        self.original_rect = self.rect.copy()
        self.clicked_offset[0] = self.rect.centerx - mouse_pos[0]
        self.clicked_offset[1] = self.rect.centery - mouse_pos[1]

    def unclick(self):
        if self.state != 'CLICK':
            return
        self.state = 'RETURN'
        self.unhover()
        if self.entering:
            self.move_original_rect()
        x, y = self.original_rect.topleft
        distance = (
            (x - self.rect.x) ** 2 + (y - self.rect.y) ** 2) ** 0.5
        distance = int(distance)
        duration = distance // self.return_speed
        if duration == 0:
            self.return_is_done()
            return
        animation = Animation(x=x, y=y, duration=duration, round_values=True)
        animation.callback = self.return_is_done
        animation.start(self.rect)
        self.animations.add(animation)

    def hover(self):
        if self.hovered or self.state == 'RETURN':
            return
        self.hovered = True
        for customer in self.customers:
            customer.hover()

    def unhover(self):
        if not self.hovered:
            return
        self.hovered = False
        for customer in self.customers:
            customer.unhover()

    def move_down(self):
        """
        When there is some space appears in queue below the customer_group,
        they need to get below.
        """
        self.entering = True
        if self.state == 'IDLE':
            self.create_entry_animation()

    def move_original_rect(self):
        if self.pause_time is None:
            self.original_rect = self.queue_rect.copy()
            return
        now = pg.time.get_ticks()
        time_elapsed = now - self.pause_time
        self.pause_time = None
        distance = time_elapsed * self.entry_speed
        self.original_rect.y += distance
        if self.original_rect.y > self.queue_rect.y:
            self.original_rect = self.queue_rect.copy()

    def return_is_done(self):
        if self.state != 'RETURN':
            return
        self.state = 'IDLE'
        if self.entering:
            self.create_entry_animation()

    def decrease_mood(self):
        self.mood -= 1
        if self.mood == 0:
            return
        elif self.mood == 1:
            self.flip_showing()
        self.mood_bar.update_image(self.mood)
        time = random.randint(*self.mood_change_time)
        task = Task(self.decrease_mood, time)
        self.tasks.add(task)

    def flip_showing(self):
        self.show = not self.show
        task = Task(self.flip_showing, 400)
        self.tasks.add(task)

    def draw(self, surface):
        if self.show:
            for customer in self.customers:
                customer.draw(surface)
        self.mood_bar.draw(surface)

    def update(self, dt, frame, mouse_pos):
        if self.state == 'IDLE' and not self.entering:
            self.tasks.update(dt * 1000)
        last_rect = self.rect.copy()
        self.animations.update(dt * 1000)
        if self.state == 'CLICK':
            self.rect.centerx = mouse_pos[0] + self.clicked_offset[0]
            self.rect.centery = mouse_pos[1] + self.clicked_offset[1]
        delta_x = self.rect.x - last_rect.x
        delta_y = self.rect.y - last_rect.y
        entry_update = self.entering and self.state == 'IDLE'
        for customer in self.customers:
            customer.rect.x += delta_x
            customer.rect.y += delta_y
            customer.update(dt, frame, entry_update)
        self.mood_bar.rect.center = self.rect.centerx, self.rect.top - 15
