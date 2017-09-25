import pygame as pg

from .. import prepare
from .animations import Animation
from .customer import Customer


class CustomerQueue(pg.sprite.Sprite):
    def __init__(self, amount, topright, start_topright=None):
        pg.sprite.Sprite.__init__(self)
        self.amount = amount
        self.customers = self.create_customers()
        self.rect = self.create_rect(start_topright)
        self.place_customers()
        self.empty_image = self.create_empty_image()
        self.update_image()
        self.animations = pg.sprite.Group()
        self.queue_rect = self.rect.copy()
        self.queue_rect.topright = topright
        self.states = []
        self.clicked_offset = [0, 0]
        self.original_rect = self.rect.copy()
        self.return_speed = 1
        self.entry_speed = 0.4
        self.entry_animation = None

    def start(self):
        self.states.append('ENTRY')
        self.create_entry_animation()

    def create_customers(self):
        customers = []
        for indx in range(self.amount):
            customer = Customer('red')
            customers.append(customer)
        return customers

    def create_rect(self, topright):
        width = self.customers[0].rect.width * self.amount
        height = self.customers[0].rect.height
        rect = pg.rect.Rect((0, 0), (width, height))
        rect.topright = topright
        return rect

    def place_customers(self):
        for indx, customer in enumerate(self.customers):
            customer.rect.topleft = (0 + indx * customer.rect.width, 0)

    def create_empty_image(self):
        image = pg.Surface((self.rect.width, self.rect.height)).convert()
        image.set_alpha(0)
        image = image.convert_alpha()
        return image

    def create_entry_animation(self):
        if self.entry_animation:
            self.entry_animation.kill()
        point = self.queue_rect.topleft
        distance = point[1] - self.rect.y
        duration = distance // self.entry_speed
        if duration == 0:
            self.entry_is_done()
            return
        self.entry_animation = Animation(
            x=point[0], y=point[1], duration=duration, round_values=True)
        self.animations.add(self.entry_animation)
        self.entry_animation.start(self.rect)
        self.entry_animation.callback = self.entry_is_done
        self.entry_animation.update_callback = self.entry_update

    def entry_update(self):
        self.original_rect = self.rect.copy()

    def pause_entry_animation(self):
        self.entry_animation.kill()
        self.pause_time = pg.time.get_ticks()
        # self.original_rect = self.queue_rect.copy()

    def entry_is_done(self):
        if self.rect.center == self.queue_rect.center:
            self.states.remove('ENTRY')
            self.states.append('IDLE')
            for customer in self.customers:
                customer.entry_is_done()
            self.update_image()
        else:
            self.create_entry_animation()

    def click(self, mouse_pos):
        if 'CLICK' in self.states:
            return
        if 'ENTRY' in self.states:
            self.pause_entry_animation()
            for customer in self.customers:
                customer.image = customer.idle_image
                self.update_image()
        for customer in self.customers:
            if customer.animate:
                pass
                # customer.stop_animation()
        if 'IDLE' in self.states:
            for customer in self.customers:
                pass
                # customer.stop_animation_timer()
        self.states.append('CLICK')
        if 'HOVER' not in self.states:
            self.states.append('HOVER')
        self.clicked_offset[0] = self.rect.centerx - mouse_pos[0]
        self.clicked_offset[1] = self.rect.centery - mouse_pos[1]

    def unclick(self):
        if 'CLICK' not in self.states:
            return
        self.states.remove('CLICK')
        self.states.append('RETURN')
        if 'ENTRY' in self.states:
            self.move_original_rect()
        x, y = self.original_rect.topleft
        distance = (
            (x - self.rect.x) ** 2 + (y - self.rect.y) ** 2) ** 0.5
        distance = int(distance)
        duration = distance // self.return_speed
        if duration == 0:
            duration = 1
        animation = Animation(x=x, y=y, duration=duration, round_values=True)
        animation.callback = self.return_is_done
        animation.start(self.rect)
        self.animations.add(animation)

    def hover(self):
        if 'HOVER' in self.states or 'CLICK' in self.states:
            return
        self.states.append('HOVER')
        if 'IDLE' in self.states:
            for customer in self.customers:
                customer.lock_hover_image()
            self.update_image()

    def unhover(self):
        if 'HOVER' not in self.states or 'CLICK' in self.states:
            return
        self.states.remove('HOVER')
        if 'IDLE' in self.states:
            for customer in self.customers:
                customer.unlock_hover_image()
            self.update_image()

    def move_down(self):
        if 'ENTRY' not in self.states:
            self.states.append('ENTRY')
        if 'IDLE' in self.states:
            self.states.remove('IDLE')
            for customer in self.customers:
                customer.idle = False
            # self.stop_animation_timer()
        for customer in self.customers:
            if customer.animate:
                pass
                # customer.stop_animation()
        if self.states == ['ENTRY']:
            self.create_entry_animation()

    def move_original_rect(self):
        now = pg.time.get_ticks()
        time_elapsed = now - self.pause_time
        distance = time_elapsed * self.entry_speed
        self.original_rect.y += distance
        if self.original_rect.y > self.queue_rect.y:
            self.original_rect = self.queue_rect.copy()

    def return_is_done(self):
        if 'RETURN' not in self.states:
            return
        self.states.remove('RETURN')
        if 'ENTRY' in self.states:
            self.create_entry_animation()
        for customer in self.customers:
            if customer.idle:
                pass
                # customer.start_animation_timer()

    def update_image(self):
        self.image = self.empty_image.copy()
        for customer in self.customers:
            self.image.blit(customer.image, customer.rect)

    def update(self, dt, frame, mouse_pos):
        self.animations.update(dt * 1000)
        if 'CLICK' in self.states:
            self.rect.centerx = mouse_pos[0] + self.clicked_offset[0]
            self.rect.centery = mouse_pos[1] + self.clicked_offset[1]
        entry_update = 'ENTRY' in self.states and 'CLICK' not in self.states
        for customer in self.customers:
            customer.update(dt, frame, entry_update)
        self.update_image()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class CustomerTable(pg.sprite.Sprite):
    def __init__(self, center, pos):
        pg.sprite.Sprite.__init__(self)
        if pos == 'LEFT':
            self.image = prepare.GFX['customers']['customer_sit']
        else:
            self.image = pg.transform.flip(
                prepare.GFX['customers']['customer_sit'], True, False)
        self.rect = self.image.get_rect(center=center)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
