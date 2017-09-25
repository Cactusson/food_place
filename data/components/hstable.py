import pickle
import pygame as pg

from .label import Label


class HSTable:
    def __init__(self):
        self.results = None
        self.image = None

    def load_table(self):
        try:
            results_file = open('results', 'rb')
            self.results = pickle.load(results_file)
        except FileNotFoundError:
            self.results = [(100000, 'OLKA', '01:00', '2 Feb 2016'),
                            (750, 'MMMMMMMMMM', '02:00', '25 Feb 2016'),
                            (555, 'VASEK', '99:25', '1 Mar 2020'), None, None]

    def save_table(self):
        results_file = open('results', 'wb')
        pickle.dump(self.results, results_file)

    def add_line(self, line):
        """
        Line should be (score, name, time, date)
        """
        if self.results[0] is not None:
            if line[0] < self.results[0][0]:
                return False
        self.results.append(line)
        self.results.sort()
        self.results.pop()
        self.save_table()
        return True

    def clear(self):
        self.results = [None, None, None, None, None]
        self.save_table()

    def create_big_image(self, center, highlighted=None):
        self.image = pg.Surface((550, 250)).convert_alpha()
        self.image.fill((0, 0, 0, 0))

        position = (0, 0)
        gap = 50
        width = 550
        height = 50
        number_x = 10
        name_x = 40
        score_x = 300
        time_x = 415
        date_x = 500

        for number, line in enumerate(self.results):
            if line is None:
                name = '-----'
                score = ''
                time = ''
                month, year = '', ''
            else:
                score, name, time, date = line
                time = '({})'.format(time)
                month, year = date[:-5], date[-4:]

            pos = (position[0], position[1] + gap * number)

            label = pg.sprite.Sprite()
            label.image = pg.Surface((width, height)).convert_alpha()
            label.image.fill((0, 0, 0, 0))
            label.rect = label.image.get_rect(topleft=pos)

            number_text = '{}.'.format(number + 1)
            number_label = Label(25, number_text, topleft=(0, 0),
                                 font_name='OpenSans-Regular')
            number_label.rect.x = number_x
            number_label.rect.centery = height // 2
            number_label.draw(label.image)

            name_text = name
            name_label = Label(25, name_text, topleft=(0, 0),
                               font_name='OpenSans-Regular')
            name_label.rect.x = name_x
            name_label.rect.centery = height // 2
            name_label.draw(label.image)

            score_text = str(score)
            score_label = Label(25, score_text, topleft=(0, 0),
                                font_name='OpenSans-Regular')
            score_label.rect.x = score_x
            score_label.rect.centery = height // 2
            score_label.draw(label.image)

            time_text = str(time)
            time_label = Label(20, time_text, topleft=(0, 0),
                               font_name='OpenSans-Regular')
            time_label.rect.x = time_x
            time_label.rect.centery = height // 2
            time_label.draw(label.image)

            month_text = str(month)
            month_label = Label(14, month_text, topleft=(0, 0),
                                font_name='OpenSans-Regular')
            month_label.rect.x = date_x
            month_label.rect.centery = height // 4
            month_label.draw(label.image)

            year_text = str(year)
            year_label = Label(14, year_text, topleft=(0, 0),
                               font_name='OpenSans-Regular')
            year_label.rect.x = date_x
            year_label.rect.centery = height // 2 + height // 4
            year_label.draw(label.image)

            if highlighted == line and line is not None:
                pg.draw.rect(label.image, pg.Color('red'),
                             (0, 0, width, height), 5)

            self.image.blit(label.image, label.rect)

        self.rect = self.image.get_rect(center=center)

    def create_small_image(self, center, underlined_line=None):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)
