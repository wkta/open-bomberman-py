import sys

from coremon_main import EventReceiver, PygameBridge

sys.path.append('..')
import eventtypes
import pygame



class ScrollText(EventReceiver):
    """
    
    """
    
    def __init__(self, font, lines=5, width=600):
        super().__init__()

        #data
        self.text = [""] # lines of text that get into the width limitation
        self.text_height = font.get_ascent() -font.get_descent()+1
        self.font = font
        self.size = (width, lines*self.text_height+4)
        self.text_field_rect = pygame.Rect(0,0,width-1, self.size[1]-1)
        self.fill_color = (220, 220, 220)
        self.text_color = (1,1,1)
        self.image = pygame.Surface(self.size).convert()
        self.text_img = pygame.Surface((width-4, lines*self.text_height)).convert()
        self.num_lines = lines
        self.cur_line = 0
        self.text_width = width-4
        
        self.render()
        self.dirty = True  # means what ??!

    def proc_event(self, ev, source):
        if ev.type == eventtypes.CHATMSG:
            self.on_chatmsg(ev)
        elif ev.type == PygameBridge.KEYDOWN:
            self.on_keydown(ev)

    def on_chatmsg(self, event):
        """
        
        """
        text = event.msg
        if self.font.size(text)[0]<self.text_width:
            self.text.append(text)
        else:
            splitted = text.split()
##            print "text1:", text
##            print "splitted:", splitted
            pos = -1
            text = ''
            for spl in splitted[:pos]:
                text += spl+' '
                
##            print "text2:", text
            while self.font.size(text)[0]>self.text_width and pos > -len(splitted):
                pos -= 1
                text = ''
                for spl in splitted[:pos]:
                    text += spl+' '
##                print "snipping text", text, pos
##            print "pos:", pos
# TODO: what if line is still too long? should be croped
            self.text.append(text)
            text = ''
            for spl in splitted[pos:]:
                text += '   '+spl
            self.text.append(text)
        self.move_pos(0)
        self.render()
        
    def on_keydown(self, event):
        """
        
        """
        if event.key == pygame.K_PAGEDOWN:
            self.move_pos(5)
        elif event.key == pygame.K_PAGEUP:
            self.move_pos(-5)
        self.render()
        
    def move_pos(self, steps=1):
        """
        
        """
        self.cur_line += steps
        if steps == 0:
            self.cur_line = len(self.text)-self.num_lines
        if self.cur_line>len(self.text)-self.num_lines:
            self.cur_line = len(self.text)-self.num_lines
        if self.cur_line<0:
            self.cur_line = 0
        
    def render(self):
        """
        
        """
        self.dirty = True
        self.image.fill(self.fill_color)
        self.text_img.fill(self.fill_color)
        ypos = 0
        line = self.cur_line
        
        num_lines = self.num_lines
        if len(self.text)<self.num_lines:
            num_lines = len(self.text)
        
            
        for num in range(num_lines):
            self.text_img.blit(\
                        self.font.render_txt(self.text[line], 2, self.text_color, \
                                             self.fill_color), (0, ypos))
            ypos += self.text_height
            line += 1
        self.image.blit(self.text_img, (2,2))
        pygame.draw.rect(self.image, (100, 100, 100), self.text_field_rect, 2)