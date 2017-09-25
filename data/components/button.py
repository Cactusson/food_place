import pygame as pg

from .. import prepare


class Button(pg.sprite.Sprite):
    """
    Button is some text on a bg. If you click on it, call (function)
    will be called.
    """
    def __init__(self, font_size, text, call, font_name=None, topleft=None,
                 center=None, blocked=False):
        pg.sprite.Sprite.__init__(self)
        self.name = text
        self.call = call
        self.blocked = blocked
        self.hover = False
        if font_name is not None:
            self.font = pg.font.Font(prepare.FONTS[font_name], font_size)
        else:
            self.font = pg.font.Font(None, font_size)
        self.idle_image, self.blocked_image, self.hover_image = \
            self.make_images(text)
        self.image = (self.idle_image if not self.blocked
                      else self.blocked_image)
        if center:
            self.rect = self.image.get_rect(center=center)
        elif topleft:
            self.rect = self.image.get_rect(topleft=topleft)
        else:
            message = 'Center or topleft should be among the kwargs of Label'
            raise ValueError(message)

    def make_images(self, text_on_button):
        """
        Button changes its image depending if the player is hovering it or not.
        """
        text_color = pg.Color('black')
        idle_color = pg.Color('#FCF0C8')
        hover_color = pg.Color('#E84A5F')
        blocked_color = pg.Color('#DCDADA')
        blocked_text_color = pg.Color('#A79E8B')
        # idle_image = self.font.render(text, True, idle_color)
        # blocked_image = self.font.render(text, True, blocked_color)
        # hover_image = self.font.render(text, True, hover_color, hover_fill)
        text = self.font.render(text_on_button, True, text_color)
        blocked_text = self.font.render(
            text_on_button, True, blocked_text_color)
        width = text.get_width() + 30
        height = text.get_height() + 20

        image = pg.Surface((width, height)).convert_alpha()
        image.fill((0, 0, 0, 0))

        idle_image = image.copy()
        small_rect = pg.rect.Rect(3, 3, width - 6, height - 6)
        pg.draw.ellipse(idle_image, idle_color, small_rect)

        blocked_image = image.copy()
        small_rect = pg.rect.Rect(3, 3, width - 6, height - 6)
        pg.draw.ellipse(blocked_image, blocked_color, small_rect)

        hover_image = image.copy()
        big_rect = pg.rect.Rect(0, 0, width, height)
        pg.draw.ellipse(hover_image, hover_color, big_rect)
        small_rect = pg.rect.Rect(3, 3, width - 6, height - 6)
        pg.draw.ellipse(hover_image, idle_color, small_rect)

        text_rect = pg.rect.Rect(0, 0, text.get_width(), text.get_height())
        text_rect.center = small_rect.center
        idle_image.blit(text, text_rect)
        blocked_image.blit(blocked_text, text_rect)
        hover_image.blit(text, text_rect)

        return idle_image, blocked_image, hover_image

    def block(self):
        self.blocked = True
        self.image = self.blocked_image

    def unblock(self):
        self.blocked = False
        mouse_pos = pg.mouse.get_pos()
        self.update(mouse_pos)

    def click(self):
        if self.hover and not self.blocked:
            if hasattr(self, 'name'):
                self.call(self.name)
            else:
                self.call()

    def update(self, mouse_pos):
        """
        Check if the button is hovered.
        """
        if self.blocked:
            return
        if hasattr(self, 'collide_rect'):
            rect = self.collide_rect
        else:
            rect = self.rect
        hover = rect.collidepoint(mouse_pos)
        if hover:
            self.image = self.hover_image
        else:
            self.image = self.idle_image
        self.hover = hover

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class ButtonPic(Button):
    """
    Same stuff as Button but with a picture, not text.
    """
    def __init__(self, idle_image, hover_image, call,
                 font_name=None, topleft=None, center=None, blocked=False,
                 blocked_image=None):
        pg.sprite.Sprite.__init__(self)
        self.call = call
        self.blocked = blocked
        self.hover = False
        self.idle_image = idle_image
        self.hover_image = hover_image
        if blocked_image:
            self.blocked_image = blocked_image
        self.image = (self.idle_image if not self.blocked
                      else self.blocked_image)
        if center:
            self.rect = self.image.get_rect(center=center)
        elif topleft:
            self.rect = self.image.get_rect(topleft=topleft)
        else:
            message = 'Center or topleft should be among the kwargs of Label'
            raise ValueError(message)
