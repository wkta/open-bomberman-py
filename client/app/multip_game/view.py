import pygame

from coremon_main import EngineEvTypes, EventReceiver
from def_gevents import MyEvTypes
from transversal.WorldSubjectMod import WorldSubjectMod


class MultipGameView(EventReceiver):

    def __init__(self, mod: WorldSubjectMod):
        super().__init__(self)
        self._bg_color = (66, 66, 66)  # red, green, blue format
        ft = pygame.font.Font(None, 19)
        self.img = ft.render('Inside the game', True, (0, 0, 0))
        self.img_pos = (200, 60)
        self._mod = mod

        self._pl_positions = list()
        self._bomb_positions = list()

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

            # entities
            for ppos in self._pl_positions:
                pygame.draw.circle(ev.screen, (10, 88, 220), ppos, 32, 0)
            for ppos in self._bomb_positions:
                pygame.draw.rect(ev.screen, (220, 11, 75), (ppos[0]-16, ppos[1]-16, 32, 32), 0)

        elif ev.type == MyEvTypes.BombsetChanges:
            del self._bomb_positions[:]
            for pos in ev.info:
                tmp = MultipGameView.game_to_scr_coords(*pos)
                self._bomb_positions.append(tmp)

        elif ev.type == MyEvTypes.PlayerMoves:
            print('view receives PlayerMoves evt')
            del self._pl_positions[:]

            for c in self._mod.irepr.list_players():
                tmp = MultipGameView.game_to_scr_coords(c[1], c[2])
                self._pl_positions.append(tmp)

    @staticmethod
    def game_to_scr_coords(i, j):
        return 15+(i*64)+32, 15+(j*64)+32
