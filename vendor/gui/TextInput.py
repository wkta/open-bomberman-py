import pygame

import coremon_main
from coremon_main import EventReceiver, PygameBridge, EngineEvTypes
from coremon_main.runners import VanillaGameCtrl


class TextInput(EventReceiver):
    """
    Simple text entry component.
    """

    _caret_color = (90, 90, 90)
    _padding = 4  # en px

    def __init__(self, nickname, font, how_to_process_cb, pos, width=300):
        """
        nickname: nickname, all messages will be prefixed with the nickname 
        font    : pygame.font.Font object
        width   : in pixel that this element can use (this restricts the number
                  of char you can enter
                
        events:
        in : pygame.KEYDOWN
        out: eventtypes.CHATMSG
        """
        super().__init__()

        self.position = pos
        # test que le 3e arg est callable...
        assert hasattr(how_to_process_cb, '__call__')
        self.on_enter_func = how_to_process_cb

        self.pwd_field = False

        # data
        self.__txt_content = ""
        self.caretpos = 0
        self.max = 255
        self.nickname = nickname

        # drawing
        self.dirty = True
        self.font = font
        height = self.font.get_ascent() - self.font.get_descent() + 1 + 4
        self.image = pygame.Surface((width, height)).convert()
        self.size = (width, height)


        self.text_color = (1, 1, 1)
        self.text_field_rect = pygame.Rect(0, 0, width - 1, height - 1)
        self.text_img = pygame.Surface((2, 2))
        self.pixel_width = width - 4

        self._focus = None
        self.fill_color = None
        self.no_focus()

    def get_disp_text(self):
        if self.pwd_field:
            return TextInput.hide_text(self.__txt_content)
        return self.__txt_content

    def focus(self):
        self._focus = True
        self.fill_color = (220, 220, 220)
        self.render_field()

    def no_focus(self):
        self._focus = False
        self.fill_color = (100, 100, 100)
        self.render_field()

    def contains(self, scr_pos):
        w, h = self.image.get_size()
        a, b = self.position[0], self.position[0] + w
        c, d = self.position[1], self.position[1] + h
        x, y = scr_pos
        if (a < x < b) and (c < y < d):
            return True
        return False

    @staticmethod
    def hide_text(txt_content):
        tmp = ['*' for i in range(len(txt_content))]
        return ''.join(tmp)

    def proc_event(self, event, source):
        if event.type != PygameBridge.KEYDOWN:
            return

        # - traitement touche pressée
        if event.key == pygame.K_RETURN:
            # self.on_enter()
            self.on_enter_func(self.__txt_content)
            self.__txt_content = ''
            self.caretpos = 0

        elif event.key == pygame.K_RIGHT:
            self.move_caret(+1)

        elif event.key == pygame.K_LEFT:
            self.move_caret(-1)

        elif event.key == pygame.K_HOME:
            self.move_caret('home')

        elif event.key == pygame.K_END:
            self.move_caret('end')

        elif event.key == pygame.K_BACKSPACE:
            self.backspace_char()

        elif event.key == pygame.K_DELETE:
            self.delete_char()

        elif event.key == pygame.K_TAB:
            pass

        else:
            if event.unicode != '':
                if len(self.__txt_content) < self.max:
                    self.__txt_content = self.__txt_content[:self.caretpos] + event.unicode + self.__txt_content[self.caretpos:]
                    self.caretpos += 1
        self.render_field()

    def move_caret(self, steps):
        """
        Moves the caret about steps. Positive numbers moves it right, negative
        numbers left.
        """
        if steps == 'home':
            self.caretpos = 0
        elif steps == 'end':
            self.caretpos = len(self.__txt_content)
        else:
            assert isinstance(steps, int)
            self.caretpos += steps

        if self.caretpos < 0:
            self.caretpos = 0
        if self.caretpos > len(self.__txt_content):
            self.caretpos = len(self.__txt_content)

    def backspace_char(self):
        """
        Deltes the char befor the caret position.
        """
        if self.caretpos > 0:
            self.__txt_content = self.__txt_content[:self.caretpos - 1] + self.__txt_content[self.caretpos:]
            self.caretpos -= 1

    def delete_char(self):
        """
        Deltes the char after the caret position.
        """
        self.__txt_content = self.__txt_content[:self.caretpos] + self.__txt_content[self.caretpos + 1:]

    def render_field(self):
        """
        Renders the string to self.image.
        """
        self.image.fill(self.fill_color)
        content = self.get_disp_text()

        if len(content):
            # while self.font.size(content)[0] > self.pixel_width:
            #    self.backspace_char()
            self.text_img = self.font.render(content, 1, self.text_color, self.fill_color)
            self.image.blit(self.text_img, (2, 2))

            # - draw caret
            xpos = self.font.size(content[:self.caretpos])[0] + 2
            pygame.draw.line(self.image, self._caret_color, (xpos, self._padding), (xpos, self.image.get_height() - self._padding), 2)
        #else:
        #    pygame.draw.line(self.image, (255, 255, 255), (3, 2), (3, self.image.get_height() - 2), 1)

        pygame.draw.rect(self.image, (100, 100, 100), self.text_field_rect, 2)


# --- DÉMO. FONCTIONNEMENT
if __name__ == '__main__':
    coremon_main.init((800, 600))
    pygame.key.set_repeat(500, 30)


    def cb(texte):
        print(texte)
        print(TextInput.hide_text(texte))


    txt_entry = TextInput("supernick:", glvars.fonts['courier_font'], cb, (100, 100))


    class BasicView(EventReceiver):
        def __init__(self, ref_te):
            super().__init__()
            self.te = ref_te

        def proc_event(self, ev, source):
            if ev.type == EngineEvTypes.PAINT:
                # print(te.text, len(te.text), te.caretpos)
                coremon_main.screen.fill((0, 0, 0))
                coremon_main.screen.blit(self.te.image, self.te.position)


    bv = BasicView(txt_entry)
    mger = coremon_main.EventManager.instance()
    bv.turn_on()
    txt_entry.turn_on()

    ctrl = VanillaGameCtrl()
    ctrl.turn_on()
    ctrl.loop()
    print('test terminé.')
