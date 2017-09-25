import pygame as pg
import random

from .. import prepare, tools
from ..components import data
from ..components.animations import Animation
from ..components.button import ButtonPic
from ..components.customers_counter import CustomersCounter
from ..components.darkness import Darkness
from ..components.hstable import HSTable
from ..components.manager import Manager
from ..components.playfield import Playfield
from ..components.scoreboard import Scoreboard
from ..components.star_bar import StarBar
from ..components.task import Task


class Game(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.tasks = pg.sprite.Group()
        self.animations = pg.sprite.Group()
        self.screen = pg.Surface(prepare.SCREEN_SIZE).convert()
        self.screen_rect = self.screen.get_rect(topleft=(0, 0))
        self.hall_rect = pg.Surface((800, 700)).convert()
        self.hall_rect.fill(pg.Color('lightgreen'))
        self.queue_surface = pg.Surface((200, 700)).convert()
        self.queue_surface.fill(pg.Color('#1A554F'))
        self.queue_rect = self.queue_surface.get_rect(topleft=(800, 0))
        self.screen_shake_points = (
            (0, 16), (0, -16), (0, 8), (0, -8), (0, 0))
        self.screen_shake_speed = 0.4
        self.screen_shake_queue = []
        self.frame = 0
        self.level_number = 1
        self.state = None
        self.bar = None
        self.darkness = None
        self.menu_screen = None
        self.star_bar = None

    def start(self):
        self.darkness = None
        self.state = 'PLAY'

    def create_level(self, first_creation=False):
        self.events = []
        self.pause_button = self.create_pause_button()
        if self.mode == 'FINITE':
            self.playfield = Playfield(
                self.mode, data.levels[self.level_number - 1]['tables'],
                self.events)
            self.scoreboard = Scoreboard(
                self.mode, self.events, level_number=self.level_number,
                data=data.levels[self.level_number - 1])
            self.manager = Manager(
                self.mode, data.levels[self.level_number - 1], self.events)
            self.customers_counter = CustomersCounter(self.mode, self.events)
        elif self.mode == 'INFINITE':
            self.playfield = Playfield(
                self.mode, data.infinite['tables'], self.events)
            self.scoreboard = Scoreboard(self.mode, self.events)
            self.manager = Manager(self.mode, data.infinite, self.events)
            self.customers_counter = CustomersCounter(self.mode, self.events)
            self.star_bar = StarBar(prepare.SCREEN_RECT.topright)

        if first_creation:
            self.scoreboard.rect.move_ip(-self.scoreboard.rect.width, 0)
            self.pause_button.rect.move_ip(-self.pause_button.rect.width, 0)
            if self.star_bar:
                self.star_bar.rect.move_ip(0, -self.star_bar.rect.height)

    def gui_appears(self):
        duration = 1000
        x, y = self.scoreboard.rect.topleft
        x += self.scoreboard.rect.width
        animation = Animation(x=x, y=y, duration=duration, round_values=True)
        animation.callback = lambda: self.tasks.add(
            Task(self.greet_player, 300))
        animation.start(self.scoreboard.rect)
        self.animations.add(animation)

        x, y = self.pause_button.rect.topleft
        x += self.pause_button.rect.width
        animation = Animation(x=x, y=y, duration=duration, round_values=True)
        animation.start(self.pause_button.rect)
        self.animations.add(animation)

        if self.star_bar:
            x, y = self.star_bar.rect.topleft
            y += self.star_bar.rect.height
            animation = Animation(x=x, y=y, duration=duration,
                                  round_values=True)
            animation.start(self.star_bar.rect)
            self.animations.add(animation)

    def create_pause_button(self):
        pause_image = tools.colorize(prepare.GFX['gui']['pause'],
                                     prepare.BUTTON_COLOR)
        image = pg.Surface((54, 54)).convert()
        idle_image = image.copy()
        idle_image.fill(prepare.FRAME_COLOR)
        idle_image.fill(prepare.FILL_COLOR, pg.rect.Rect(3, 3, 48, 48))
        idle_image.blit(pause_image, (3, 3))
        hover_image = image.copy()
        hover_image.fill(prepare.FRAME_COLOR)
        hover_image.fill(pg.Color('green'), pg.rect.Rect(3, 3, 48, 48))
        hover_image.blit(pause_image, (3, 3))
        button = ButtonPic(idle_image, hover_image, self.pause_game,
                           topleft=(0, 155))
        return button

    def change_level(self, win):
        """
        If win == True, then move on to the next level.
        (If there are no more levels, then to_continue is set to False)
        If win == False, stay on the same level.
        """
        self.to_continue = True
        if win:
            self.level_number += 1
            self.victory = True
        else:
            self.victory = False
        if self.level_number > len(data.levels):
            self.to_continue = False

    def screen_shake_start(self):
        self.screen_shake_queue = list(self.screen_shake_points)
        self.screen_shake_next()

    def screen_shake_next(self):
        if not self.screen_shake_queue:
            return
        x, y = self.screen_shake_queue.pop(0)
        distance = ((y - self.screen_rect.y) ** 2) ** 0.5
        duration = distance // self.screen_shake_speed
        if duration == 0:
            duration = 1
        animation = Animation(x=x, y=y, duration=duration, round_values=True)
        animation.callback = self.screen_shake_next
        animation.start(self.screen_rect)
        self.animations.add(animation)

    def check_events(self):
        for event in self.events:
            name, args = event[0], event[1:]
            if name == 'LEVEL FINISHED':
                task = Task(lambda: self.events.append(('END OF LEVEL',)), 300)
                self.tasks.add(task)
            elif name == 'END OF LEVEL':
                if self.mode == 'FINITE':
                    win = self.scoreboard.score >= self.scoreboard.goal
                    self.level_finished(win)
                elif self.mode == 'INFINITE':
                    self.infinite_mode_game_over()
            elif name == 'TIMER FINISHED':
                self.playfield.close()
            elif name == 'ADD SCORE':
                if len(args) == 1:
                    deal = args[0]
                    mood = None
                else:
                    deal, mood = args
                points, combo_text = self.scoreboard.add_score(deal, mood)
                self.playfield.waiter.create_flying_label(points, combo_text)
            elif name == 'ADD COLOR SCORE':
                seat = args[0]
                self.scoreboard.add_color_score(
                    seat.color_bonus * seat.color_multiplier)
                seat.create_flying_label(
                    seat.color_bonus * seat.color_multiplier)
                seat.grow_color_multiplier()
                seat.color_bonus = None
            elif name == 'ADD CUSTOMER':
                if self.playfield.open:
                    colors = args[0]
                    success = self.playfield.create_customer(colors)
                    if success:
                        self.manager.create_customer_task()
                    else:
                        self.manager.customer_short_interval()
            elif name == 'ADD UFO':
                if not self.playfield.ufo:
                    self.playfield.create_ufo()
                    self.manager.create_ufo_task()
                else:
                    self.manager.ufo_short_interval()
            elif name == 'ADD ROBBER':
                if not self.playfield.robber:
                    self.playfield.create_robber()
                    self.manager.create_robber_task()
                else:
                    self.manager.robber_short_interval()
            elif name == 'UFO ARRIVED':
                self.screen_shake_start()
            elif name == 'CUSTOMER SERVED':
                self.customers_counter.customer_is_served()
            elif name == 'CUSTOMER LOST':
                self.customers_counter.customer_is_lost()
                if self.mode == 'INFINITE':
                    self.star_bar.destroy_star()
            elif name == 'WAITER TOOK MEAL':
                number = args[0]
                for table in self.playfield.tables:
                    if table.number == number:
                        table.flag.fire_up()
        self.events[:] = []

    def level_finished(self, win):
        self.change_level(win)
        self.show_player_out()

    def infinite_mode_game_over(self):
        self.show_player_out()

    def create_info_dict_start(self):
        if self.mode == 'FINITE':
            level_data = data.levels[self.level_number - 1]
        elif self.mode == 'INFINITE':
            level_data = data.infinite
        info_dict = level_data['info_dict']
        if 'goal' in level_data:
            info_dict['goal'] = level_data['goal']
        return info_dict

    def create_info_dict_end(self):
        more_rounds_ahead = self.to_continue
        if self.victory:
            title = 'LEVEL {} IS FINISHED'.format(self.level_number - 1)
        else:
            title = 'FAIL'
        text = ('Score: {}'.format(self.scoreboard.score),
                'Customers served: {}'.format(
                    self.customers_counter.customers_served),
                'Customers lost: {}'.format(
                    self.customers_counter.customers_lost))
        buttons = ('OK',)
        info_dict = {
            'more_rounds_ahead': more_rounds_ahead,
            'title': title,
            'text': text,
            'buttons': buttons,
        }
        return info_dict

    def create_info_dict_inf(self):
        title = 'GAME OVER'
        text = ('Your score: {}'.format(self.scoreboard.score),
                'Time played: {}'.format(self.scoreboard.timer.time_to_text()),
                )
        buttons = ('HS', 'RESTART', 'QUIT')
        info_dict = {
            'title': title,
            'text': text,
            'buttons': buttons,
        }
        return info_dict

    def pause_game(self):
        self.flip_state('PAUSE')

    def flip_state(self, new_state):
        self.next = new_state
        self.done = True
        if new_state == 'MESSAGE_SCREEN':
            self.persist['screen'] = pg.display.get_surface().copy()
            if self.state == 'PLAY':
                if self.mode == 'FINITE':
                    self.persist['info_dict'] = self.create_info_dict_end()
                elif self.mode == 'INFINITE':
                    score_data = self.add_score_to_hs()
                    self.persist['info_dict'] = self.create_info_dict_inf()
                    self.persist['info_dict']['score_data'] = score_data
            elif self.state == 'FROZEN':
                self.persist['info_dict'] = self.create_info_dict_start()
        elif new_state == 'PAUSE':
            self.persist['screen'] = pg.display.get_surface().copy()

    def add_score_to_hs(self):
        hstable = HSTable()
        hstable.load_table()
        line = (self.scoreboard.score, 'ABC',
                self.scoreboard.timer.time_to_text(), '1 Feb 2016')
        success = hstable.add_line(line)
        hstable.save_table()
        if success:
            return line
        else:
            return False

    def waiter_restarted_callback(self):
        self.start()
        self.darkness.start_growing()

    def create_darkness_and_stuff(self):
        self.darkness = Darkness(self.create_level, self.greet_player)
        self.darkness.start_shrinking()

    def slide_screen(self):
        self.state = 'FROZEN'
        self.bar = pg.sprite.Sprite()
        self.bar.image = pg.Surface((100, prepare.SCREEN_RECT.height))
        self.bar.image.fill(pg.Color('brown'))
        self.bar.rect = self.bar.image.get_rect(
            topleft=(prepare.SCREEN_RECT.right, 0))
        x = -self.bar.rect.width - 25
        y = self.bar.rect.y
        animation = Animation(x=x, y=y, duration=1500, transition='out_quad',
                              round_values=True)
        animation.callback = self.gui_appears
        animation.update_callback = self.slide_screen_update_callback
        animation.start(self.bar.rect)
        self.slide_screen_rect = prepare.SCREEN_RECT.copy()
        self.animations.add(animation)

    def slide_screen_update_callback(self):
        width = self.bar.rect.left
        height = self.bar.rect.height
        rect = pg.rect.Rect(0, 0, width, height)
        rect.normalize()
        self.slide_screen_rect = rect

    def greet_player(self):
        self.bar = None
        self.menu_screen = None
        self.flip_state('MESSAGE_SCREEN')
        self.state = 'PLAY'

    def show_player_out(self):
        self.flip_state('MESSAGE_SCREEN')
        self.state = 'FROZEN'

    def update_frame(self):
        self.frame += 1
        if self.frame % 4 == 0:
            self.frame = 0

    def startup(self, persistant):
        self.persist = persistant
        if self.previous == 'PAUSE':
            pass
        elif self.previous == 'CHOOSE_LEVEL':
            self.menu_screen = self.persist['menu_screen']
            del self.persist['menu_screen']
            self.mode = 'FINITE'
            self.level_number = self.persist['level_number']
            del self.persist['level_number']
            self.create_level(True)
            self.slide_screen()
        elif self.previous == 'MAIN_MENU':
            self.menu_screen = self.persist['menu_screen']
            del self.persist['menu_screen']
            self.mode = 'INFINITE'
            self.create_level(True)
            self.slide_screen()
        elif self.previous == 'MESSAGE_SCREEN':
            if self.state == 'FROZEN':
                self.create_darkness_and_stuff()
        else:
            self.start()

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
            elif event.key == pg.K_q:
                self.pause_game()
            elif event.key == pg.K_SPACE:
                amount = random.randint(1, 4)
                colors = [random.choice(['red', 'blue', 'green'])
                          for _ in range(amount)]
                self.playfield.queue.add_customer(colors)
            elif event.key == pg.K_0:
                self.playfield.queue.add_customer(
                    ('red', 'green', 'green', 'red'))
            elif event.key == pg.K_a:
                self.screen_shake_start()
            elif event.key == pg.K_b:
                if self.playfield.ufo:
                    self.playfield.ufo.depart(self.playfield.event_ufo_is_gone)
                else:
                    self.playfield.create_ufo()
            elif event.key == pg.K_w:
                self.playfield.create_firearm()
            elif event.key == pg.K_e:
                self.playfield.create_robber()
            elif event.key == pg.K_1:
                self.level_finished(True)
            elif event.key == pg.K_2:
                self.level_finished(False)
            elif event.key == pg.K_3:
                print(self.customers_counter.customers_served,
                      self.customers_counter.customers_lost)
        elif event.type == pg.MOUSEBUTTONDOWN:
            if self.state == 'FROZEN':
                return
            if event.button == 1:
                self.playfield.event_mouse_click(event.pos)
                self.pause_button.click()
        elif event.type == pg.MOUSEBUTTONUP:
            if self.state == 'FROZEN':
                return
            self.playfield.event_click_release(event.pos)

    def draw(self, surface):
        self.screen.blit(self.hall_rect, (0, 0))
        self.screen.blit(self.queue_surface, self.queue_rect)
        self.playfield.draw(self.screen)
        self.scoreboard.draw(self.screen)
        if self.star_bar:
            self.star_bar.draw(self.screen)
        self.pause_button.draw(self.screen)
        if self.state == 'FROZEN':
            if self.darkness:
                self.darkness.draw(self.screen)
            if self.menu_screen:
                self.screen.blit(
                    self.menu_screen, (0, 0), self.slide_screen_rect)
            if self.bar:
                self.screen.blit(self.bar.image, self.bar.rect)
        surface.fill(pg.Color('black'))
        surface.blit(self.screen, self.screen_rect)

    def update(self, surface, current_time, dt):
        mouse_pos = pg.mouse.get_pos()
        self.tasks.update(dt * 1000)
        self.animations.update(dt * 1000)
        self.pause_button.update(mouse_pos)
        if self.state == 'PLAY':
            # self.animations.update(dt * 1000)
            self.update_frame()
            self.check_events()
            self.scoreboard.update(dt)
            self.manager.update(dt)
            self.playfield.update(self.frame, dt, mouse_pos)
        elif self.state == 'FROZEN':
            if self.darkness:
                self.darkness.update(self.playfield.waiter.rect.center, dt)
        self.draw(surface)
