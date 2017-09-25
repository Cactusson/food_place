# import itertools
import pygame as pg
import random

from .. import prepare
from .bubble import Bubble
# from .customers import CustomerTable
from .customer import Customer
from .flag import Flag
from .label import Label
from .mood_bar import MoodBar
from .order import Order
from .seat import Seat
from .task import Task


class Table(pg.sprite.Sprite):
    image_dict = {
        4: prepare.GFX['table_simple']['table_big'],
        2: prepare.GFX['table_simple']['table_small'],
    }

    def __init__(self, midtop, entry, number, seat_colors):
        """
        Table can have 2 seats (small) or 4 seats (big).
        Every seat can be a different color or can have no color.
        seat_colors goes [TOPLEFT, TOPRIGHT] for small one, or
        [TOPLEFT, TOPRIGHT, BOTTOMLEFT, BOTTOMRIGHT] for big one.
        """
        pg.sprite.Sprite.__init__(self)
        self.tasks = pg.sprite.Group()
        self.number = number
        # self.idle_image = prepare.GFX['table']['table']
        # self.image_customers = prepare.GFX['table']['table_customers']
        # self.image_dirty = prepare.GFX['table']['table_dirty']
        # self.images_eating = itertools.cycle(
        #     [prepare.GFX['table']['table_eating_{}'.format(i)]
        #      for i in range(1, 4)])
        self.size = len(seat_colors)
        self.image = self.image_dict[self.size]
        self.rect = self.image.get_rect(midtop=midtop)
        self.entry = entry
        self.seats = self.create_seats(seat_colors)
        self.click_rect = self.rect.unionall(
            [seat.rect for seat in self.seats])
        self.flag = Flag(self.number, self.rect)
        # self.customers = []
        self.bubble_center = self.rect.centerx, self.rect.top - 50
        self.bubble = None
        self.change_state('FREE')
        self.hovered = False
        self.color_bonus_label = None
        self.mood = None
        self.mood_bar = None
        self.mark = None  # marks are created in Waiter

    def create_seats(self, colors):
        seats = pg.sprite.Group()
        locations = ((self.rect.left - 50, self.rect.top),
                     (self.rect.right, self.rect.top),
                     (self.rect.left - 50, self.rect.top + 50),
                     (self.rect.right, self.rect.top + 50))
        for topleft, color in zip(locations, colors):
            seat = Seat(topleft, color)
            seats.add(seat)
        return seats

    def assume_customers(self, customer_group):
        # customer = CustomerTable(self.rect.midleft, 'LEFT')
        # self.customers = [customer]
        # if customer_group.amount == 2:
        #     customer = CustomerTable(self.rect.midright, 'RIGHT')
        #     self.customers.append(customer)
        customers = [
            Customer(customer.color) for customer in customer_group.customers]
        seated_customers = []
        colored_seats = [seat for seat in self.seats if seat.color != 'none']
        colored_seats.sort(reverse=True,
                           key=lambda seat: seat.color_multiplier)
        for seat in colored_seats:
            for customer in customers:
                if customer in seated_customers:
                    continue
                if customer.color == seat.color:
                    seat.get_customer(customer)
                    seated_customers.append(customer)
                    break
        for customer in customers:
            free_seats = [seat for seat in self.seats if seat.customer is None]
            if customer in seated_customers or not free_seats:
                continue
            same_color = [seat for seat in free_seats
                          if seat.color == customer.color]
            same_color.sort(reverse=True,
                            key=lambda seat: seat.color_multiplier)
            no_color = [seat for seat in free_seats if seat.color == 'none']
            diff_color = [
                seat for seat in free_seats
                if seat.color != customer.color and seat.color != 'none']
            diff_color.sort(key=lambda seat: seat.color_multiplier)
            free_seats = same_color + no_color + diff_color
            seat = free_seats[0]
            seat.get_customer(customer)
        # for customer, seat in zip(customers, self.seats):
        #     seat.get_customer(customer)
        self.create_color_bonus_label()
        self.mood = customer_group.mood
        self.mood_bar = MoodBar((self.rect.centerx, self.rect.bottom),
                                self.mood)

    def unassume_customers(self):
        if self.state == 'FREE':
            for seat in self.seats:
                seat.empty()
            self.mood = None
            self.mood_bar = None

    def sit_customers(self):
        self.change_state('CHOOSING')
        for seat in self.seats:
            if seat.customer:
                seat.sit_customer()
        self.unhover()

    def create_color_bonus_label(self):
        bonus = sum([seat.color_bonus * seat.color_multiplier
                     for seat in self.seats if seat.color_bonus])
        if bonus == 0:
            return
        center = self.rect.centerx, self.rect.centery - 85
        self.color_bonus_label = Label(35, str(bonus), center=center)

    def change_state(self, new_state):
        self.state = new_state
        self.update_label()
        if self.state == 'FREE':
            pass
            # self.image = self.idle_image
        if self.state == 'CHOOSING':
            # self.image = self.image_customers
            time = random.randint(3, 5) * 1000
            task = Task(self.change_state, time, args=('READY_TO_ORDER',))
            self.tasks.add(task)
        elif self.state == 'READY_TO_ORDER':
            self.bubble = Bubble(self.bubble_center, 'order')
        elif self.state == 'WAITING':
            self.bubble = None
        elif self.state == 'EATING':
            self.flag.back_to_normal()
            self.increase_mood(1)
            time = random.randint(5, 8) * 1000
            task = Task(self.change_state, time, args=('READY_TO_PAY',))
            self.tasks.add(task)
        elif self.state == 'READY_TO_PAY':
            # self.image = self.image_customers
            self.bubble = Bubble(self.bubble_center, 'money')
        elif self.state == 'DIRTY':
            # self.image = self.image_dirty
            self.mood = None
            self.mood_bar = None
            self.bubble = None
            for seat in self.seats:
                seat.empty()

    def produce_order(self):
        order = Order(self.number)
        return order

    def check_if_empty(self):
        return self.state == 'FREE'

    def hover(self, customer_group):
        if (self.hovered or not customer_group or
                customer_group.amount > self.size):
            return
        self.assume_customers(customer_group)
        self.hovered = True

    def unhover(self):
        if not self.hovered:
            return
        self.hovered = False
        self.color_bonus_label = None
        self.unassume_customers()

    def increase_mood(self, amount):
        if self.mood == 5:
            return
        self.mood += amount
        self.mood_bar.update_image(self.mood)

    def update_label(self):
        center = self.rect.centerx, self.rect.top - 15
        self.label = Label(25, self.state, center=center, bg=pg.Color('white'))

    def update_image(self, frame):
        if frame != 0:
            return

        self.image = next(self.images_eating)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for seat in self.seats:
            seat.draw(surface)
        self.label.draw(surface)
        if self.state == 'WAITING':
            self.flag.draw(surface)
        if self.bubble:
            self.bubble.draw(surface)
        if self.color_bonus_label:
            self.color_bonus_label.draw(surface)
        if self.mood_bar:
            self.mood_bar.draw(surface)
        if self.mark:
            self.mark.draw(surface)

    def update(self, dt, frame, mouse_pos, clicked_customer):
        self.tasks.update(dt * 1000)
        if self.state == 'FREE':
            if self.click_rect.collidepoint(mouse_pos):
                self.hover(clicked_customer)
            else:
                self.unhover()
        self.seats.update(dt)
        # if self.state == 'EATING':
        #     self.update_image(frame)
