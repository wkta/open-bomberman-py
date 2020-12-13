import pygame

from coremon_main import EngineEvTypes, EventReceiver
from defs_bombm import MyEvTypes
from transversal.LocalWorld import LocalWorld


class MultipGameView(EventReceiver):

    def __init__(self, mod: LocalWorld):
        super().__init__(self)
        self._bg_color = (66, 66, 66)  # red, green, blue format
        ft = pygame.font.Font(None, 19)
        self.img = ft.render('Inside the game', True, (0, 0, 0))
        self.img_pos = (200, 60)
        self._mod = mod
        self._pl_positions = []

    # override
    def proc_event(self, ev, source=None):
        if ev.type == EngineEvTypes.PAINT:
            ev.screen.fill(self._bg_color)
            ev.screen.blit(self.img, self.img_pos)

            # grid
            ax, ay = 15, 15
            offsetpx = 64
            lim = self._mod.gridsize
            for i in range(lim+1):
                tmp = ax+i*offsetpx
                pygame.draw.line(ev.screen, (15, 192, 50), (tmp, ay), (tmp, ay+lim*offsetpx))
            for j in range(lim+1):
                tmp = ay+j*offsetpx
                pygame.draw.line(ev.screen, (15, 192, 50), (ax, tmp), (ax+lim*offsetpx, tmp))

            if len(self._pl_positions):
                for ppos in self._pl_positions:
                    pygame.draw.circle(ev.screen, (10, 88, 220), ppos, 32)

        elif ev.type == MyEvTypes.PlayerMoves:
            print('view receives PlayerMoves evt')
            del self._pl_positions[:]

            for c in self._mod.irepr.state.values():
                tmp = MultipGameView.game_to_scr_coords(*c)
                print(tmp)
                self._pl_positions.append(tmp)

    @staticmethod
    def game_to_scr_coords(i, j):
        return 15+(i*64)+32, 15+(j*64)+32
