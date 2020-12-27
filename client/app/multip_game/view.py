import pygame

import glvars
import gui
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

        self._player_infos = list()
        self._bomb_positions = list()
        self._wall_positions = list()
        self._blocks_positions = list()

        self._refresh_block_n_walls()

        # wait text
        ft = pygame.font.Font(None, 77)
        titlepos = [glvars.SCR_SIZE[0] // 2, glvars.SCR_SIZE[1] // 2]
        titlepos[1] -= glvars.SCR_SIZE[1] // 3
        self._plz_wait_label = gui.Text(
            'Waiting for other players... Please wait', ft, titlepos, anchortype=gui.Text.ANCHOR_CENTER
        )

    def _refresh_block_n_walls(self):
        del self._blocks_positions[:]
        for wpos in self._mod.irepr.blocks_locations():
            tmp_coords = MultipGameView.game_to_scr_coords(wpos[0], wpos[1])
            self._blocks_positions.append(tmp_coords)

        del self._wall_positions[:]
        for wpos in self._mod.irepr.wall_locations():
            tmp_coords = MultipGameView.game_to_scr_coords(wpos[0], wpos[1])
            self._wall_positions.append(tmp_coords)

    def _draw_game_entities(self, scr):
        # - DRAW ALL entities
        bluecol = (10, 88, 220)
        darkgreen = (25, 85, 25)
        redcolor = (220, 11, 75)
        graycolor = (196, 196, 196)

        # draw walls
        for ppos in self._wall_positions:
            pygame.draw.rect(scr, bluecol, (ppos[0] - 30, ppos[1] - 30, 60, 60), 0)

        # draw blocks
        for ppos in self._blocks_positions:
            pygame.draw.rect(scr, darkgreen, (ppos[0] - 30, ppos[1] - 30, 60, 60), 0)

        # draw players
        for i, j, plcolor in self._player_infos:
            pygame.draw.circle(scr, plcolor, (i, j), 32, 0)

        # draw bombs
        for ppos in self._bomb_positions:
            pygame.draw.circle(scr, graycolor, ppos, 24, 0)

    # override
    def proc_event(self, ev, source=None):

        if ev.type == EngineEvTypes.PAINT:
            ev.screen.fill(self._bg_color)
            # ev.screen.blit(self.img, self.img_pos)

            # draw grid
            ax, ay = 15, 15
            offsetpx = glvars.CELL_SIZE_PX
            xlim, ylim = self._mod.gridsize
            for i in range(xlim + 1):
                tmp = ax + i * offsetpx
                pygame.draw.line(ev.screen, (15, 192, 50), (tmp, ay), (tmp, ay + ylim * offsetpx))
            for j in range(ylim + 1):
                tmp = ay + j * offsetpx
                pygame.draw.line(ev.screen, (15, 192, 50), (ax, tmp), (ax + xlim * offsetpx, tmp))

            self._draw_game_entities(ev.screen)

            # draw txt
            if self._plz_wait_label:
                self._plz_wait_label.paint(ev.screen)

        elif ev.type == MyEvTypes.ChallengeStarts:
            self._plz_wait_label = None

        elif ev.type == MyEvTypes.BombsetChanges:
            # - refresh bombs
            del self._bomb_positions[:]
            for pos in ev.info:
                tmp = MultipGameView.game_to_scr_coords(*pos)
                self._bomb_positions.append(tmp)

            self._refresh_block_n_walls()

        elif ev.type == MyEvTypes.PlayerMoves:
            print('view receives PlayerMoves evt')
            del self._player_infos[:]

            for tripletinfos in self._mod.irepr.all_players_position():
                plcode, i, j = tripletinfos
                ip, jp = MultipGameView.game_to_scr_coords(i, j)
                color = MultipGameView.color_from_plcode(plcode)
                self._player_infos.append((ip, jp, color))

    @staticmethod
    def color_from_plcode(x: int):
        return (17*x) % 255, (x - 158) % 255, (39*x+111) % 255

    @staticmethod
    def game_to_scr_coords(i, j):
        return 15+(i*64)+32, 15+(j*64)+32
