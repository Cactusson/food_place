import pygame as pg

from .. import prepare
from .animations import Animation
from .task import Task


class Label(pg.sprite.Sprite):
    """
    Just some text.
    """
    def __init__(self, font_size, text, font_name=None, color=None,
                 center=None, topleft=None, bg=None, width=None,
                 height=None, antialias=True):
        pg.sprite.Sprite.__init__(self)
        if font_name is not None:
            self.font = pg.font.Font(prepare.FONTS[font_name], font_size)
        else:
            self.font = pg.font.Font(None, font_size)
        if color is not None:
            self.color = color
        else:
            self.color = pg.Color('black')
        self.text = text
        self.image = self.make_image(antialias, bg, width, height)
        if center:
            self.rect = self.image.get_rect(center=center)
        elif topleft:
            self.rect = self.image.get_rect(topleft=topleft)
        else:
            message = 'Center or topleft should be among the kwargs of Label'
            raise ValueError(message)

    def make_image(self, antialias, bg, width, height):
        if width and height:
            image = pg.Surface((width, height)).convert()
            if bg:
                image.fill(bg)
            else:
                image.set_alpha(0)
                image = image.convert_alpha()
            text = self.font.render(self.text, antialias, self.color)
            rect = text.get_rect(center=(width // 2, height // 2))
            image.blit(text, rect)
        else:
            image = self.font.render(self.text, antialias, self.color, bg)
        return image

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class MultiLineLabel(pg.sprite.Sprite):
    """
    Creates a single surface with multiple labels blitted to it.
    """
    def __init__(self, font_size, text, font_name=None, color=None,
                 center=None, topleft=None, bg=None, antialias=True,
                 char_limit=40, align='center', vert_space=0):
        pg.sprite.Sprite.__init__(self)
        lines = self.wrap_text(text, char_limit)
        labels = [Label(font_size, line, center=(0, 0),
                        font_name=font_name, color=color, bg=bg,
                        antialias=antialias) for line in lines]
        width = max([label.rect.width for label in labels])
        spacer = vert_space * (len(lines) - 1)
        height = sum([label.rect.height for label in labels])+spacer
        self.image = pg.Surface((width, height)).convert()
        self.image.set_alpha(0)
        self.image = self.image.convert_alpha()
        if center is not None:
            self.rect = self.image.get_rect(center=center)
        elif topleft is not None:
            self.rect = self.image.get_rect(topleft=topleft)
        else:
            message = 'Center or topleft should be among the kwargs of Label'
            raise ValueError(message)
        aligns = {"left": {"left": 0},
                  "center": {"centerx": self.rect.width // 2},
                  "right": {"right": self.rect.width}}
        y = 0
        for label in labels:
            label.rect = label.image.get_rect(**aligns[align])
            label.rect.top = y
            label.draw(self.image)
            y += label.rect.height + vert_space

    def wrap_text(self, text, char_limit, separator=" "):
        """
        Splits a string into a list of strings no longer than char_limit.
        """
        words = text.split(separator)
        lines = []
        current_line = []
        current_length = 0
        for word in words:
            if len(word) + current_length <= char_limit:
                current_length += len(word) + len(separator)
                current_line.append(word)
            else:
                lines.append(separator.join(current_line))
                current_line = [word]
                current_length = len(word) + len(separator)
        if current_line:
            lines.append(separator.join(current_line))
        return lines

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class FlyingLabel(pg.sprite.Sprite):
    def __init__(self, font_size, text, center, color=None):
        pg.sprite.Sprite.__init__(self)
        self.animations = pg.sprite.Group()
        self.tasks = pg.sprite.Group()
        self.label = self.make_label(font_size, text, center, color)
        self.alpha = 255
        self.alpha_step = 40
        self.label.image.set_alpha(self.alpha)
        x = self.label.rect.x
        y = self.label.rect.y - 40
        animation = Animation(
            x=x, y=y, duration=1500, round_values=True,
            transition='out_quad')
        animation.callback = self.disappear
        animation.start(self.label.rect)
        self.animations.add(animation)

    def make_label(self, font_size, text, center, color):
        if color:
            label = Label(
                font_size, text, center=center, color=pg.Color(color),
                antialias=False, font_name='OpenSans-Regular')
        else:
            label = Label(font_size, text, center=center, antialias=False,
                          font_name='OpenSans-Regular')
        return label

    def disappear(self):
        if self.alpha == 0:
            self.kill()
            return
        self.alpha = max(0, self.alpha - self.alpha_step)
        self.label.image.set_alpha(self.alpha)
        task = Task(self.disappear, 100)
        self.tasks.add(task)

    def draw(self, surface):
        self.label.draw(surface)

    def update(self, dt):
        self.animations.update(dt * 1000)
        self.tasks.update(dt * 1000)
