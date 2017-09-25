import pygame as pg

from ..components.board import Board
from ..components.dish import Dish
from ..components.firearm import Firearm
from ..components.meal import Meal
from ..components.order import Order
from ..components.orderbox import Orderbox
from ..components.queue import Queue
from ..components.robber import Robber
from ..components.stand import Stand
from ..components.table import Table
from ..components.ufo import UFO
from ..components.waiter import Waiter
from ..components.washbox import Washbox


class Playfield:
    def __init__(self, mode, tables, game_events):
        self.mode = mode
        self.game_events = game_events

        tables_active = [(True if table is not None else False)
                         for table in tables]
        self.board = Board(tables_active)
        self.tables = self.create_tables(tables)
        self.washbox = Washbox(
            self.board.washbox_pos, self.board.washbox_entry)
        self.orderbox = Orderbox(
            self.board.orderbox_pos, self.board.orderbox_entry)
        self.stand = Stand(
            self.board.stand_pos, self.board.meal_1_entry,
            self.board.meal_2_entry)
        self.waiter = Waiter(self.board)
        self.queue = Queue()
        self.ufo = None
        self.firearm = None
        self.robber = None
        self.meals = pg.sprite.Group()

        self.clickable_objs = pg.sprite.Group(
            self.tables, self.washbox, self.orderbox)
        self.open = True
        # self.waiter = None
        self.on = True

    def create_tables(self, tables_list):
        tables = pg.sprite.Group()
        count = 0
        for seats, entry in zip(tables_list, self.board.table_positions):
            if seats is not None:
                count += 1
                rect = pg.rect.Rect(0, 0, 185, 100)
                rect.center = entry
                rect.y += 75
                # seat_colors = seats
                table = Table(rect.midtop, entry, count, seats)
                tables.add(table)
        return tables

    def create_customer(self, colors):
        return self.queue.add_customer(colors)

    def create_ufo(self):
        if not self.open:
            return
        entry = self.board.ufo_pos
        center = entry[0], entry[1] - 100
        self.ufo = UFO(center, entry)
        self.ufo.arrive(self.event_ufo_is_here)

    def create_firearm(self):
        if not self.open:
            return
        entry = self.board.firearm_pos
        self.firearm = Firearm((380, 60), entry)
        self.clickable_objs.add(self.firearm)

    def create_robber(self):
        if not self.open:
            return
        center = (900, 50)
        path = [(900, 150), (850, 150)]
        entry = self.board.robber_pos
        self.robber = Robber(center, entry, path)
        self.clickable_objs.add(self.robber)
        if self.firearm is None:
            self.create_firearm()

    def create_meal(self, number):
        meal = self.stand.add_meal(number)
        if meal:
            self.clickable_objs.add(meal)
            self.meals.add(meal)

    def event_ufo_is_here(self):
        self.game_events.append(('UFO ARRIVED',))
        self.ufo.change_state('READY_TO_ORDER')
        self.clickable_objs.add(self.ufo)
        self.board.ufo_arrived_corrections()

    def event_ufo_is_gone(self):
        self.ufo = None
        self.board.ufo_departed_corrections()

    def event_firearm_is_gone(self):
        self.firearm = None

    def event_click_on_obj(self, obj):
        if isinstance(obj, Meal):
            callback = self.waiter_to_meal
        elif isinstance(obj, Table):
            callback = self.waiter_to_table
        elif isinstance(obj, UFO):
            callback = self.waiter_to_ufo
        elif isinstance(obj, Orderbox):
            callback = self.waiter_to_orderbox
        elif isinstance(obj, Washbox):
            callback = self.waiter_to_washbox
        elif isinstance(obj, Firearm):
            callback = self.waiter_to_firearm
        elif isinstance(obj, Robber):
            callback = self.waiter_to_robber
        else:
            callback = None
        self.waiter.add_to_queue(obj, callback)

    def event_mouse_click(self, mouse_pos):
        self.queue.click(mouse_pos)
        if self.on:
            for obj in self.clickable_objs:
                if hasattr(obj, 'click_rect'):
                    click_rect = obj.click_rect
                else:
                    click_rect = obj.rect
                if click_rect.collidepoint(mouse_pos):
                    self.event_click_on_obj(obj)
                    break

    def event_click_release(self, pos):
        if self.queue.clicked_customer:
            self.queue.clicked_customer.unclick()
            for table in self.tables:
                if table.state == 'FREE' and table.hovered:
                    self.customers_to_table(self.queue.clicked_customer, table)
                    break
            self.queue.clicked_customer = None

    def waiter_to_meal(self, meal):
        if self.waiter.has_empty_hand():
            self.game_events.append(('WAITER TOOK MEAL', meal.number))
            self.stand.clear_meal(meal)
            self.waiter.hand_take(meal)
            meal.kill()

    def waiter_to_table(self, table):
        if table.state == 'READY_TO_ORDER':
            if self.waiter.has_empty_hand():
                order = table.produce_order()
                self.waiter.hand_take(order)
                table.change_state('WAITING')
                self.game_events.append(('ADD SCORE', 'ORDER'))
        elif table.state == 'WAITING':
            for hand in self.waiter.hands:
                if isinstance(hand, Meal):
                    if hand.number == table.number:
                        table.change_state('EATING')
                        self.waiter.hand_remove(hand)
                        self.game_events.append(('ADD SCORE', 'MEAL'))
                        break
        elif table.state == 'READY_TO_PAY':
            self.game_events.append(('ADD SCORE', 'PAY', table.mood))
            self.game_events.append(('CUSTOMER SERVED',))
            table.change_state('DIRTY')
        elif table.state == 'DIRTY':
            if self.waiter.has_empty_hand():
                dish = Dish()
                self.waiter.hand_take(dish)
                table.change_state('FREE')
                self.game_events.append(('ADD SCORE', 'DISH'))

    def waiter_to_ufo(self, ufo):
        if ufo.state == 'READY_TO_ORDER':
            if self.waiter.has_empty_hand():
                order = ufo.produce_order()
                self.waiter.hand_take(order)
                ufo.change_state('WAITING')
                self.game_events.append(('ADD SCORE', 'ORDER'))
        elif ufo.state == 'WAITING':
            for hand in self.waiter.hands:
                if isinstance(hand, Meal):
                    if hand.number == ufo.number:
                        self.waiter.hand_remove(hand)
                        self.game_events.append(('ADD SCORE', 'MEAL'))
                        self.game_events.append(('ADD SCORE', 'PAY'))
                        self.clickable_objs.remove(ufo)
                        ufo.depart(self.event_ufo_is_gone)
                        break

    def waiter_to_orderbox(self, orderbox):
        for hand in self.waiter.hands:
            if isinstance(hand, Order) and self.stand.able_to_add_meal():
                self.create_meal(hand.number)
                self.waiter.hand_remove(hand)

    def waiter_to_washbox(self, washbox):
        for hand in self.waiter.hands:
            if isinstance(hand, Dish):
                self.waiter.hand_remove(hand)

    def waiter_to_firearm(self, firearm):
        if firearm.state == 'READY':
            if self.waiter.both_hands_are_empty():
                firearm.empty()
                self.waiter.take_rifle()
        elif firearm.state == 'EMPTY':
            for hand in self.waiter.hands:
                if str(hand) == 'FIREARM':
                    self.waiter.leave_rifle()
                    if self.robber:
                        firearm.load()
                    else:
                        firearm.disappear(self.event_firearm_is_gone)
                    break

    def waiter_to_robber(self, robber):
        for hand in self.waiter.hands:
            if str(hand) == 'FIREARM':
                self.waiter.rifle.start_shooting()
                self.clickable_objs.remove(robber)
                self.robber = None
                break

    def customers_to_table(self, customer_group, table):
        self.queue.remove_customer(customer_group)
        for seat in table.seats:
            if seat.color_bonus:
                self.game_events.append(
                    ('ADD COLOR SCORE', seat))
        table.sit_customers()

    def close(self):
        self.open = False

    def restart(self):
        animation = self.waiter.move_back()
        # self.queue.clear()
        return animation

    def check_if_finished(self):
        if self.open:
            return
        if not self.queue.check_if_empty():
            return
        for table in self.tables:
            if not table.check_if_empty():
                return
        if not self.waiter.both_hands_are_empty():
            return
        if self.ufo:
            return
        if self.robber:
            return

        self.finish()

    def finish(self):
        self.on = False
        self.waiter.clear()
        if self.mode == 'FINITE':
            self.game_events.append(('LEVEL FINISHED',))

    def draw(self, surface):
        self.stand.draw(surface)
        self.orderbox.draw(surface)
        self.washbox.draw(surface)
        if self.firearm:
            self.firearm.draw(surface)
        if self.ufo:
            self.ufo.draw(surface)
        self.waiter.draw(surface)
        for table in self.tables:
            table.draw(surface)
        if self.robber:
            self.robber.draw(surface)
        for meal in self.meals:
            meal.draw(surface)
        table_hovered = any([table.hovered for table in self.tables])
        self.queue.draw(surface, table_hovered)
        # self.board.draw(surface)

    def update(self, frame, dt, mouse_pos):
        if self.mode == 'FINITE':
            self.check_if_finished()
        if self.on:
            self.tables.update(
                dt, frame, mouse_pos, self.queue.clicked_customer)
            if self.firearm:
                self.firearm.update(dt)
            if self.ufo:
                self.ufo.update(dt)
            if self.robber:
                self.robber.update(dt)
            self.queue.update(dt, frame, mouse_pos, self.game_events)
            self.orderbox.update(mouse_pos)
            self.washbox.update(mouse_pos)

        self.waiter.update(dt, frame)
