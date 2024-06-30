import sys

import pygame

from coremon_main import EventReceiver, PygameBridge


sys.path.append('..')


def test_func():
    print( "Button clicked!")


class HybridButton(EventReceiver):

    HIDEOUS_PURPLE = (255, 0, 255)

    def __init__(self, font, text, position_on_screen, draw_background, callback, *args):
        super().__init__()
        padding_value = 20  # pixels

        if draw_background:
            self.bg_color = (100, 100, 100)
            self.fg_color = (255, 255, 255)
        else:
            self.bg_color = self.HIDEOUS_PURPLE
            self.fg_color = (0, 0, 0)

        # data
        self._callback = callback
        self._args = args

        self._text = text
        self._hit = False
        
        # dawing
        self.font = font
        self.txt = text
        size = font.size(text)
        self.tmp_size = size
        self.position = position_on_screen
        self._col_rect = pygame.Rect(self.position, size).inflate(padding_value, padding_value)
        self._col_rect.topleft = self.position
        
        self.image = None
        self.refresh_img()

    def refresh_img(self):
        self.image = pygame.Surface(self._col_rect.size).convert()
        self.image.fill(self.bg_color)

        if self.bg_color != self.HIDEOUS_PURPLE:
            textimg = self.font.render(self.txt, True, self.fg_color, self.bg_color)
        else:
            textimg = self.font.render(self.txt, False, self.fg_color)
        xpos = (self._col_rect.width - self.tmp_size[0]) / 2
        ypos = (self._col_rect.height - self.tmp_size[1]) / 2
        self.image.blit(textimg, (xpos, ypos))

        if self.bg_color == self.HIDEOUS_PURPLE:
            self.image.set_colorkey((self.bg_color))
            box_color = (190,)*3
            full_rect = (0, 0, self.image.get_size()[0], self.image.get_size()[1])
            pygame.draw.rect(self.image, box_color, full_rect, 1)

    # pour des raisons pratiques (raccourci)
    def get_size(self):
        return self.image.get_size()

    def proc_event(self, ev, source):
        if ev.type == PygameBridge.KEYDOWN:
            self.on_keydown(ev)
        elif ev.type == pygame.MOUSEMOTION:
            self.on_mousemotion(ev)
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            self.on_mousedown(ev)
        elif ev.type == pygame.MOUSEBUTTONUP:
            self.on_mouseup(ev)

    def on_keydown(self, event):
        """
        Decides what do to with a keypress.
        special meanings have these keys: 
        enter, left, right, home, end, backspace, delete
        """
        if event.type != pygame.KEYDOWN:
            print( "textentry got wrong event: " + str(event))
        else:
            self.render()
### debug
            # if __name__=='__main__' and event.key == pygame.K_ESCAPE:
            #     events.RootEventSource.instance().stop()
        
    def on_mousedown(self, event):
        pos = event.pos
        if self._col_rect.collidepoint(pos):
            self._hit = True

    def on_mouseup(self, event):
##        print "mouse button up", event.pos
##        print self._up_col_rect
##        print self._down_col_rect
        pos = event.pos
        if self._hit and self._col_rect.collidepoint(pos):
            if self._callback:
                if self._args:
                    self._callback(*self._args)
                else:
                    self._callback()
        self._hit = False
        
    def on_mousemotion(self, event):
        pass
        
    def set_callback(self, callback):
        self._callback = callback
        
    def render(self):
        """
        
        """
        pass
        
    def update(self):
        """
        Actually not needed. (only need if this module is run as a script)
        """
        # only need if this module is run as a script
        if __name__ == '__main__':
##            print "_min_w:", self._min_w, "len items:", len(self._items)
            screen = pygame.display.get_surface()
            screen.fill( (100, 0, 0))
            screen.blit(self.image, self.position)
##            pygame.draw.rect(screen, (255,255,0), self._text_col_rect, 1)
##            pygame.draw.rect(screen, (255,255,0), self._up_col_rect, 1)
##            pygame.draw.rect(screen, (255,255,0), self._down_col_rect, 1)
            pygame.display.flip()


# if __name__ == '__main__':
#     pygame.init()
#     pygame.key.set_repeat(500, 30)
#     pygame.display.set_mode((800,600))
#     t = Button(pygame.font.Font(None, 30), "cancel", (100,100), test_func)
#
# ##    tt = Spinner(pygame.font.Font(None, 30), (300,100))
# ##    tt.add(Item("Human", 1))
# ##    tt.add(Item("passive AI", 2))
# ##    tt.add(Item("dumb AI", 3))
# ##    tt.add(Item("better AI", 4))
# ##    tt.add(Item("None", 5))
#
#     events.RootEventSource.instance().add_listener(t)
#     print( t.parent)
#     events.RootEventSource.instance().set_blocking(True)
#     events.RootEventSource.instance().run(t.update)
    
