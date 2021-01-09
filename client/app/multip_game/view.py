import pygame
import os
import glvars
import gui
from coremon_main import EngineEvTypes, EventReceiver
from def_gevents import MyEvTypes
from transversal.SpriteSheet import SpriteSheet
from transversal.WorldSubjectMod import WorldSubjectMod


class MultipGameView(EventReceiver):

    def __init__(self, mod: WorldSubjectMod):
        super().__init__(self)

        self.bomb_color = (3, 16, 8)
        self._bg_color = (66, 66, 66)  # red, green, blue format
        ft = pygame.font.Font(None, 19)
        self.img = ft.render('Inside the game', True, (0, 0, 0))
        self.img_pos = (200, 60)
        self._mod = mod

        # load assets...
        def open_sprsheet(filename):
            with open(filename, 'r') as myimg:
                surff = pygame.image.load(myimg)
                return SpriteSheet(surff, (16, 16), pygame.color.Color('blue'), upscaling=4)

        # -- load ASSETS (tileset, avatars) --
        tileset = open_sprsheet(os.path.join('..', 'assets', 'tileset.png'))

        self.floor_spr = tileset[369]  # ou 553 pour du sol plus clair
        self.weakwall_spr = tileset[342]
        self.invblock_spr = tileset[370]

        self.avatar_sprsheets = {
            0: open_sprsheet(os.path.join('..', 'assets', 'avatar0.png')),
            1: open_sprsheet(os.path.join('..', 'assets', 'avatar1.png')),
            2: open_sprsheet(os.path.join('..', 'assets', 'avatar2.png')),
            3: open_sprsheet(os.path.join('..', 'assets', 'avatar3.png')),
        }
        self.__plcode_to_gfxid = dict()

        # -- end load assets

        self._player_infos = list()
        self._bomb_positions = list()
        self._weakwall_positions = list()
        self._invblock_positions = list()

        self._refresh_block_n_walls()

        # wait text
        ft = pygame.font.Font(None, 77)
        titlepos = [glvars.SCR_SIZE[0] // 2, glvars.SCR_SIZE[1] // 2]
        titlepos[1] -= glvars.SCR_SIZE[1] // 3
        self._plz_wait_label = gui.Text(
            'Waiting for other players... Please wait', ft, titlepos, anchortype=gui.Text.ANCHOR_CENTER
        )

    def update_player_gfx(self, plcode, gfxid):
        print('setting plcode - gfxid association: {} {}'.format(plcode, gfxid))
        self.__plcode_to_gfxid[plcode] = gfxid

    def _refresh_block_n_walls(self):
        del self._invblock_positions[:]
        for wpos in self._mod.irepr.blocks_locations():
            tmp_coords = MultipGameView.game_to_scr_coords(wpos[0], wpos[1])
            self._invblock_positions.append(tmp_coords)

        del self._weakwall_positions[:]
        for wpos in self._mod.irepr.wall_locations():
            tmp_coords = MultipGameView.game_to_scr_coords(wpos[0], wpos[1])
            self._weakwall_positions.append(tmp_coords)

    def _debug_draw_game_entities(self, scr):
        # - DRAW ALL entities
        bluecol = (10, 88, 220)
        darkgreen = (25, 85, 25)
        redcolor = (220, 11, 75)
        graycolor = (196, 196, 196)

        # draw walls
        for ppos in self._weakwall_positions:
            pygame.draw.rect(scr, bluecol, (ppos[0] - 30, ppos[1] - 30, 60, 60), 0)

        # draw blocks
        for ppos in self._invblock_positions:
            pygame.draw.rect(scr, darkgreen, (ppos[0] - 30, ppos[1] - 30, 60, 60), 0)

        # draw players
        for i, j, plcolor in self._player_infos:
            pygame.draw.circle(scr, plcolor, (i, j), 32, 0)

        # draw bombs
        for ppos in self._bomb_positions:
            pygame.draw.circle(scr, graycolor, ppos, 24, 0)

    def _draw_gamescreen(self, surf):
        surf.fill(self._bg_color)
        # ev.screen.blit(self.img, self.img_pos)

        # draw grid
        # ax, ay = 15, 15
        # offsetpx = glvars.CELL_SIZE_PX
        basex, basey = 15, 15
        xlim, ylim = self._mod.gridsize
        # for i in range(xlim + 1):
        #     tmp = ax + i * offsetpx
        #     pygame.draw.line(surf, (15, 192, 50), (tmp, ay), (tmp, ay + ylim * offsetpx))
        # for j in range(ylim + 1):
        #     tmp = ay + j * offsetpx
        #     pygame.draw.line(surf, (15, 192, 50), (ax, tmp), (ax + xlim * offsetpx, tmp))

        # - draw floor n grid
        sq = glvars.CELL_SIZE_PX
        for i in range(xlim):
            for j in range(ylim):
                ppos = (basex + i*sq, basey + j*sq)
                surf.blit(self.floor_spr, ppos)

        # - DRAW ALL entities
        for ppos in self._weakwall_positions:  # walls (destructible)
            targetpos = (ppos[0] - 30, ppos[1] - 30, 60, 60)
            surf.blit(self.weakwall_spr, targetpos)

        for ppos in self._invblock_positions:  # blocks (invicible)
            targetpos = (ppos[0] - 30, ppos[1] - 30, 60, 60)
            surf.blit(self.invblock_spr, targetpos)

        for scrx, scry, plcode in self._player_infos:  # players
            if plcode not in self.__plcode_to_gfxid:  # late sync fix...
                self.__plcode_to_gfxid[plcode] = self._mod.getgfxid(plcode)

            # general case
            temp = self.__plcode_to_gfxid[plcode]
            adhoc_img = self.avatar_sprsheets[temp][0]
            surf.blit(adhoc_img, (scrx, scry))

            # - debug
            # pygame.draw.circle(surf, plcolor, (i, j), 32, 0)

        for ppos in self._bomb_positions:  # bombs
            pygame.draw.circle(surf, self.bomb_color, ppos, 24, 0)

        # draw txt
        if self._plz_wait_label:
            self._plz_wait_label.paint(surf)

    # override
    def proc_event(self, ev, source=None):

        if ev.type == EngineEvTypes.PAINT:
            self._draw_gamescreen(ev.screen)

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
                self._player_infos.append((ip-glvars.CELL_SIZE_PX//2, jp-glvars.CELL_SIZE_PX//2, plcode))

    @staticmethod
    def color_from_plcode(x: int):
        return (17*x) % 255, (x - 158) % 255, (39*x+111) % 255

    @staticmethod
    def game_to_scr_coords(i, j):
        return 15+(i*64)+32, 15+(j*64)+32
