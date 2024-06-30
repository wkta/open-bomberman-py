import pygame


class Text:

    ANCHOR_TL_CORNER, ANCHOR_CENTER = range(2)

    def __init__(self, text, font, position, anchortype=None):
        self.text = text
        self._position = position

        if anchortype is None:
            anchortype = self.ANCHOR_TL_CORNER

        size = font.size(text)
        rect = pygame.Rect((0, 0), size)
        self.image = pygame.Surface(rect.size).convert()
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))

        txtimg = font.render(text, False, (255, 255, 255), (0, 0, 0))  # cant use antialias or it blends with bg color
        xpos = (rect.width - size[0]) / 2
        ypos = (rect.height - size[1]) / 2
        self.image.blit(txtimg, (xpos, ypos))

        # compute the drawposition
        if self.ANCHOR_TL_CORNER == anchortype:
            self._draw_position = self._position
        else:
            self._draw_position = int(self._position[0] - size[0]/2), int(self._position[1] - size[1]/2)
        # - debug
        # print(self.drawposition)

    def paint(self, surface):
        surface.blit(self.image, self.drawposition)

    @property
    # -- DEPRECATED, lets keep it only for back-compatibility --
    def position(self):
        print('*warning deprecated method called*')
        return self._position
    
    @property
    def drawposition(self):
        return self._draw_position
