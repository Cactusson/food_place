import pygame as pg

from .. import prepare

from .checkmark import Checkmark
from .label import Label
from .level_label import LevelLabel
from .timer import Timer


class Scoreboard(pg.sprite.Sprite):
    def __init__(self, mode, game_events, level_number=None, data=None,
                 width=200, height=150):
        """
        Scoreboard shows different info for different mode.
        In FINITE and BONUS it shows your goal score and time left.
        In FINITE it also shows level number.
        In INFINITE it shows a stopwatch that just goes on and on.
        It shows your current score in all modes.
        """
        pg.sprite.Sprite.__init__(self)
        self.mode = mode
        self.game_events = game_events
        self.image = self.create_empty_image(width, height)
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.last_deal = None
        self.score = 0
        self.score_dict = {'ORDER': 10,
                           'MEAL': 20,
                           'DISH': 30,
                           'PAY': (40, 60, 80, 100)}
        self.update_score_label()
        if self.mode == 'INFINITE':
            self.timer = Timer('STOPWATCH')
            self.goal = None
            self.goal_label = None
            self.level_label = None
        elif self.mode == 'FINITE':
            self.level_label = LevelLabel(level_number, (30, 30))
            time = data['time']
            self.goal = data['goal']
            self.timer = Timer('COUNTDOWN', time, self.timer_callback)
            self.goal_label = Label(
                22, 'GOAL: {}'.format(self.goal), topleft=(35, 70),
                font_name='OpenSans-Regular')
            self.goal_met = False
        self.checkmark = None
        self.timer.start()

    def create_empty_image(self, width, height):
        image = pg.Surface((width, height)).convert()
        image.fill(prepare.FRAME_COLOR)
        image.fill(prepare.FILL_COLOR, rect=pg.rect.Rect(5, 5, 50, 50))
        image.fill(prepare.FILL_COLOR, rect=pg.rect.Rect(60, 5, 135, 50))
        image.fill(prepare.FILL_COLOR, rect=pg.rect.Rect(5, 60, 190, 85))
        return image

    def add_score(self, deal, mood):
        points = self.score_dict[deal]
        if deal == 'PAY':
            if mood is not None:
                points = points[mood - 2]
            else:
                points = points[-1]
        if not self.last_deal:
            self.last_deal = [deal, 2]
            combo_text = ''
        elif self.last_deal[0] == deal:
            if deal == 'PAY':
                points += 40 * (self.last_deal[1] - 1)
            else:
                points *= self.last_deal[1]
            combo_text = 'COMBO: {} x {}'.format(self.last_deal[1], deal)
            self.last_deal[1] += 1
        else:
            self.last_deal = [deal, 2]
            combo_text = ''
        self.score += points
        self.update_score_label()
        if self.mode == 'FINITE' and not self.goal_met:
            self.check_if_goal_is_met()
        return points, combo_text

    def add_color_score(self, points):
        self.score += points
        self.update_score_label()
        if self.mode == 'FINITE' and not self.goal_met:
            self.check_if_goal_is_met()

    def check_if_goal_is_met(self):
        if self.score >= self.goal:
            self.goal_met = True
            self.create_checkmark()

    def create_checkmark(self):
        center = self.goal_label.rect.right + 22, self.goal_label.rect.centery
        self.checkmark = Checkmark(center=center)

    def timer_callback(self):
        self.game_events.append(('TIMER FINISHED', ))

    def update_score_label(self):
        if self.mode == 'FINITE':
            topleft = (35, 105)
        elif self.mode == 'INFINITE':
            topleft = (35, 90)
        text = 'SCORE: {}'.format(self.score)
        self.score_label = Label(22, text, topleft=topleft,
                                 font_name='OpenSans-Regular')

    def draw(self, surface):
        image = self.image.copy()
        self.score_label.draw(image)
        self.timer.draw(image)
        if self.goal_label:
            self.goal_label.draw(image)
        if self.level_label:
            self.level_label.draw(image)
        if self.checkmark:
            self.checkmark.draw(image)
        surface.blit(image, self.rect)

    def update(self, dt):
        self.timer.update(dt)
