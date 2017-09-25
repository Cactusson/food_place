import pygame as pg

from .customer_group import CustomerGroup


class Queue:
    def __init__(self):
        self.customers = pg.sprite.LayeredUpdates()
        self.entry_point = (1000, 0)
        self.gap = 100
        first_position = (1000, 500)
        self.places = [(first_position[0], first_position[1] - self.gap * indx)
                       for indx in range(5)]
        self.free = [True, True, True, True, True]
        self.clicked_customer = None

    def clear(self):
        """
        Deletes all customers. The queue will not work properly after that,
        it will have to be recreated.
        """
        self.customers.empty()

    def add_customer(self, colors):
        for (place, free) in zip(self.places, self.free):
            if free:
                self.free[self.places.index(place)] = False
                customer_location = place
                break
        else:
            return False
        customer = CustomerGroup(colors, customer_location, self.entry_point)
        self.customers.add(customer)
        self.customers.move_to_back(customer)
        customer.start()
        return True

    def remove_customer(self, customer):
        customers = self.customers.sprites()
        to_move = customers[:customers.index(customer)]
        customer.kill()
        if to_move:
            place = to_move[0].queue_rect.topright
        else:
            place = customer.queue_rect.topright
        self.free[self.places.index(place)] = True
        for customer in to_move:
            customer.queue_rect.y += self.gap
            customer.move_down()

    def get_customer(self, pos):
        customers = self.customers.get_sprites_at(pos)
        if customers:
            customer = customers[-1]
            return customer

    def check_if_empty(self):
        return not self.customers

    def check_hover(self, mouse_pos):
        customer = self.get_customer(mouse_pos)
        if customer:
            customer.hover()
        for cust in self.customers:
            if cust != customer:
                cust.unhover()

    def click(self, mouse_pos):
        customer = self.get_customer(mouse_pos)
        if customer:
            self.clicked_customer = customer
            customer.click(mouse_pos)

    def draw(self, surface, table_hovered):
        for customer in self.customers:
            if customer != self.clicked_customer:
                customer.draw(surface)
        if self.clicked_customer and not table_hovered:
            self.clicked_customer.draw(surface)

    def update(self, dt, frame, mouse_pos, game_events):
        for customer in self.customers:
            if customer.mood == 0:
                self.remove_customer(customer)
                game_events.append(('CUSTOMER LOST',))
        if not self.clicked_customer:
            self.check_hover(mouse_pos)
        self.customers.update(dt, frame, mouse_pos)
