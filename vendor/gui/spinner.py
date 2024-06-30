import sys

from coremon_main import EventReceiver, PygameBridge

sys.path.append('..')
import eventtypes
import pygame


class Item(object):
    """
    
    """
    
    def __init__(self, text, value):
        """
        
        """
        object.__init__(self)
        self.text = text
        self.value = value


class Spinner(EventReceiver):
    """
    
    """
    
    def __init__(self, font, position_on_screen, cyclic=True):
        super().__init__()
        # data
        self._items = []
        self._idx = -1
        self._hit = False
        self._observers = []
        self._cyclic = cyclic
        
        # dawing
        self.font = font
        self.image = pygame.Surface((0,0))
        self.position = position_on_screen
        self._min_w = 1
        self._h = font.get_ascent() - self.font.get_descent()+1+4
        self._up_img = pygame.Surface((font.size("<")[0], self._h))
##        self._up_img.fill((100,100,100))
        self._up_img.blit( \
                self.font.render("<", 2, (255, 255, 255), (0, 0, 0)), (0, 0))
        self._up_img.convert()
##        self._up_img.set_colorkey((0,0,0))
        self._down_img = pygame.Surface((font.size(">")[0], self._h))
##        self._down_img.fill((100,100,100))
        self._down_img.blit( \
                 self.font.render(">", 1, (255, 255, 255), (0, 0, 0)),(0, 0))
        self._down_img.convert()
        self._down_img.set_colorkey((0,0,0))
        
        self.render()

    def proc_event(self, ev, source):
        if ev.type == PygameBridge.KEYDOWN:
            self.on_keydown(ev)
        elif ev.type == PygameBridge.MOUSEMOTION:
            self.on_mousedown(ev)
        elif ev.type == PygameBridge.MOUSEBUTTONDOWN:
            self.on_mousedown(ev)
        elif ev.type == PygameBridge.MOUSEBUTTONUP:
            self.on_mouseup(ev)

    def on_keydown(self, event):
        """
        Decides what do to with a keypress.
        """
        if event.type != pygame.KEYDOWN:
            print( "textentry got wrong event:" + str(event))
        else:
            self.render()
### debug
            # if __name__=='__main__' and event.key == pygame.K_ESCAPE:
            #     events.RootEventSource.instance().stop()
        
    def on_mousedown(self, event):
        """
        
        """
        pos = event.pos
        if self._down_col_rect.collidepoint(pos) or \
        self._up_col_rect.collidepoint(pos) or \
        self._text_col_rect.collidepoint(pos):
            self._hit = True

        
    def on_mouseup(self, event):
        """
        
        """
##        print "mouse button up", event.pos
##        print self._up_col_rect
##        print self._down_col_rect
        pos = event.pos
        if self._hit:
            if self._down_col_rect.collidepoint(pos):
##                print "spin down"
                self.spin_down()
            elif self._up_col_rect.collidepoint(pos):
                self.spin_up()
            elif self._text_col_rect.collidepoint(pos):
##                print "spin up"
                if event.button in [1,2,5]:
                    self.spin_up()
                else:
                    self.spin_down()
##            print "idx:", self._idx
        self._hit = False
        
    def on_mousemotion(self, event):
        """
        
        """
        pass
        
    def add(self, item):
        """
        
        """
        self._items.append(item)
        if self._idx == -1:
            self._idx = 0
        for item in self._items:
            ww = self.font.size(item.text)[0]+4
            if self._min_w < ww:
                self._min_w = ww
        self.render()
        
    def remove(self, item):
        """
        
        """
        pass
        
    def get_current_index(self):
        """
        
        """
        return self._idx
        
    def get_current_item(self):
        """
        
        """
        return self._items[self._idx]
    
    def get_current_value(self):
        """
        
        """
        return self._items[self._idx].value
        
    def spin_up(self):
        """
        
        """
        self._idx += 1
        if self._cyclic:
            self._idx %= len(self._items)
        else:
            if self._idx >= len(self._items):
                self._idx = len(self._items)-1
        self.render()
        self.notify_observers()
        
    def spin_down(self):
        """
        
        """
        self._idx -= 1
        if self._cyclic:
            self._idx %= len(self._items)
        else:
            if self._idx <= 0:
                self._idx = 0
        self.render()
        self.notify_observers()
        
    def register_observer(self, observer):
        """
        
        """
        self._observers.append(observer)
        
    def remove_observer(self, observer):
        """
        
        """
        try:
            self._observers.remove(observer)
        except:
            pass
            
    def notify_observers(self):
        """
        
        """
        for observer in self._observers:
            observer.notify(self)
        
    def render(self):
        """
        
        """
        w = self._min_w+self._down_img.get_width()+self._up_img.get_width()
        h = self._h

        # update collision rects
        self._down_col_rect = pygame.Rect(self.position, self._up_img.get_size())

        tmp_pos = (self.position[0] + self._min_w +self._up_img.get_width() , self.position[1])
        self._up_col_rect = pygame.Rect(tmp_pos, self._down_img.get_size())

        self._text_col_rect = pygame.Rect(self.position[0]+self._up_img.get_width(), \
                                self.position[1], self._min_w, self._h )

        # draw
        self.image = pygame.Surface((w, h )).convert()
        # self.image.fill((200,200,200))
        self.image.set_colorkey((0,0,0))
        self.image.blit(self._up_img, (0,0))
        self.image.blit(self._down_img, (self._up_img.get_width()+self._min_w,0))
        if len(self._items):
            img = self.font.render(self._items[self._idx].text, 1, \
                                       (255,255,255), (0,0,0))
            ww = (self._min_w-img.get_width())/2
            self.image.blit(img , (self._up_img.get_width()+ww,0))
        
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
#     t = Spinner(pygame.font.Font(None, 30), (100,100))
#     t.add(Item("Human", 1))
#     t.add(Item("passive AI", 2))
#     t.add(Item("dumb AI", 3))
#     t.add(Item("better AI", 4))
#     t.add(Item("None", 5))
#
#     events.RootEventSource.instance().add_listener(t)
#     print( t.parent)
#     events.RootEventSource.instance().set_blocking(True)
#     events.RootEventSource.instance().run(t.update)

# -- junk
##    tt = Spinner(pygame.font.Font(None, 30), (300,100))
##    tt.add(Item("Human", 1))
##    tt.add(Item("passive AI", 2))
##    tt.add(Item("dumb AI", 3))
##    tt.add(Item("better AI", 4))
##    tt.add(Item("None", 5))