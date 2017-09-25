import itertools
import pygame as pg

from .. import prepare
from .animations import Animation
from .label import FlyingLabel, Label
from .mark import Mark
from .firearm import Rifle


class Waiter(pg.sprite.Sprite):
    def __init__(self, board):
        pg.sprite.Sprite.__init__(self)
        self.get_path = board.get_path
        self.image_idle = prepare.GFX['waiter_new']['waiter']
        self.images_walking = itertools.cycle(
            [prepare.GFX['waiter_new']['waiter_walking_{}'.format(i)]
             for i in range(1, 5)])
        self.image = self.image_idle
        self.rect = self.image.get_rect(center=board.waiter_pos)
        self.original_topleft = self.rect.topleft
        self.animations = pg.sprite.Group()
        self.hands = [None, None]
        self.labels = pg.sprite.Group()
        self.update_labels()
        self.queue = []
        self.idle = True
        self.speed = 0.4
        self.return_speed = 0.6
        self.rifle = None
        self.moving = False
        self.flying_labels = pg.sprite.Group()
        self.flying_labels_offsets = (-20, -45)
        self.target = None
        self.clear()

    def has_empty_hand(self):
        for hand in self.hands:
            if hand is None:
                return True
        return False

    def both_hands_are_empty(self):
        for hand in self.hands:
            if hand is not None:
                return False
        return True

    def hand_take(self, obj):
        for indx in range(len(self.hands)):
            if self.hands[indx] is None:
                self.hands[indx] = obj
                self.update_labels()
                break

    def hand_remove(self, obj):
        for indx in range(len(self.hands)):
            if str(self.hands[indx]) == str(obj):
                self.hands[indx] = None
                self.update_labels()

    def update_labels(self):
        left = Label(25, 'LEFT: {}'.format(self.hands[0]), topleft=(25, 600),
                     bg=pg.Color('white'))
        right = Label(25, 'RIGHT: {}'.format(self.hands[1]), topleft=(25, 625),
                      bg=pg.Color('white'))
        self.labels.empty()
        self.labels.add(left, right)

    # def move_back(self):
    #     for hand in self.hands:
    #         if hand is not None:
    #             self.hand_remove(hand)
    #     self.clear()
    #     self.stop_moving()
    #     x, y = self.original_topleft
    #     distance = ((self.rect.x - x) ** 2 + (self.rect.y - y) ** 2) ** 0.5
    #     duration = distance // self.return_speed
    #     if duration <= 0:
    #         duration = 1
    #     animation = Animation(x=x, y=y, duration=duration, round_values=True)
    #     animation.start(self.rect)
    #     return animation

    def clear(self):
        self.callback = None
        self.path = None
        self.animations.empty()
        if self.target:
            self.target.mark = None
            self.target = None
        self.moving = False
        self.image = self.image_idle

    def create_mark(self, obj):
        obj.mark = Mark(obj.rect.center)

    def add_to_queue(self, target, callback=None):
        self.queue.append((target, callback))
        self.create_mark(target)
        if self.idle is True:
            self.next_in_queue()

    def next_in_queue(self):
        if not self.queue:
            self.idle = True
            return
        self.idle = False
        target, callback = self.queue.pop(0)
        if not target.alive():
            self.clear()
            self.next_in_queue()
            return
        self.target = target
        self.callback = callback
        self.start_moving(target.entry)

    def start_moving(self, target_pos):
        self.path = self.get_path(self.rect.center, target_pos)
        if self.path:
            self.moving = True
            self.animations.empty()
            self.next_animation()
        else:
            self.path_is_done()

    def next_animation(self):
        if self.path:
            x, y = self.path.pop(0)
            x -= self.rect.width // 2
            y -= self.rect.height // 2
            distance = x - self.rect.x + y - self.rect.y
            distance = (distance ** 2) ** 0.5
            duration = distance // self.speed
            if duration == 0:
                self.path_is_done()
                return
            animation = Animation(
                x=x, y=y, duration=duration, round_values=True)
            animation.callback = self.next_animation
            if self.rifle:
                animation.update_callback = self.rifle_update
            animation.start(self.rect)
            self.animations.add(animation)
        else:
            self.path_is_done()

    def path_is_done(self):
        """
        After the waiter reaches his target.
        """
        if self.callback:
            self.callback(self.target)
        self.clear()
        self.next_in_queue()

    def take_rifle(self):
        """
        Takes rifle, this function should only be called if
        self.both_hands_are_empty() is True.
        """
        self.hand_take('FIREARM')
        self.hand_take('FIREARM')
        self.rifle = Rifle(self.rect.center)

    def leave_rifle(self):
        for hand in self.hands:
            self.hand_remove(hand)
        self.rifle = None

    def rifle_update(self):
        self.rifle.rect.center = self.rect.center

    def create_flying_label(self, points, combo_text=''):
        if combo_text:
            text = '{}'.format(combo_text)
            center = (self.rect.centerx,
                      self.rect.top + self.flying_labels_offsets[0])
            label_combo = FlyingLabel(28, text, center=center)
            self.flying_labels.add(label_combo)
            points_offset = self.flying_labels_offsets[1]
        else:
            points_offset = self.flying_labels_offsets[0]
        text = '+{}'.format(points)
        center = (self.rect.centerx, self.rect.top + points_offset)
        label_points = FlyingLabel(28, text, center=center)
        self.flying_labels.add(label_points)

    def update_image(self, frame):
        if frame != 0:
            return
        self.image = next(self.images_walking)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for label in self.labels:
            label.draw(surface)
        if self.hands[0] and self.hands[0] != 'FIREARM':
            rect = self.hands[0].rect.copy()
            rect.center = self.rect.topleft
            surface.blit(self .hands[0].image, rect)
        if self.hands[1] and self.hands[1] != 'FIREARM':
            rect = self.hands[1].rect.copy()
            rect.center = self.rect.topright
            surface.blit(self .hands[1].image, rect)
        if self.rifle:
            self.rifle.draw(surface)
        for label in self.flying_labels:
            label.draw(surface)

    def update(self, dt, frame):
        self.animations.update(dt * 1000)
        if self.rifle:
            self.rifle.update(frame)
        if self.moving:
            self.update_image(frame)
        for label in self.flying_labels:
            label.update(dt)
