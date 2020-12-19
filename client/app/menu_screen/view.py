import pygame

import glvars
import gui
from coremon_main import EngineEvTypes, EventReceiver
from defs_bombm import MyEvTypes


class MenuScreenView(EventReceiver):

    def __init__(self, mod):
        super().__init__(self)
        self._bg_color = (66, 66, 177)  # rgb format

        ft = pygame.font.Font(None, 77)
        titlepos = [glvars.SCR_SIZE[0] // 2, glvars.SCR_SIZE[1] // 2]
        titlepos[1] -= (2 ** 7 + 2 ** 5)
        self.label = gui.Text('~ {} ~'.format(glvars.GAME_TITLE), ft, titlepos, anchortype=gui.Text.ANCHOR_CENTER)

        self._small_ft = pygame.font.Font(None, 24)
        line_spacing_modes = 68  # px

        self._texts = [
            'solo game',
            'multiplayer game',
            'server config',
            'quit'
        ]
        self._curr_texts = list(self._texts)
        self._nb_modes = len(self._curr_texts)
        self._mode_positions = [
            (glvars.SCR_SIZE[0] // 2, 200 + i * line_spacing_modes) for i in range(self._nb_modes)
        ]
        self.lbl_modes = list()

        # retrieve the selcted mode...
        sm = mod.selection
        self._curr_texts[sm] = MenuScreenView.tag_selected_mode(self._texts[sm])
        self.refresh_labels()

    def refresh_labels(self):
        del self.lbl_modes[:]
        for i in range(self._nb_modes):
            lbl = gui.Text(
                self._curr_texts[i], self._small_ft, self._mode_positions[i], anchortype=gui.Text.ANCHOR_CENTER
            )
            self.lbl_modes.append(lbl)

    @staticmethod
    def tag_selected_mode(mode_str):
        return '<##>   {}   <##>'.format(mode_str)

    def proc_event(self, ev, source=None):

        if ev.type == EngineEvTypes.PAINT:
            ev.screen.fill(self._bg_color)
            self.label.paint(ev.screen)
            for i in range(self._nb_modes):
                self.lbl_modes[i].paint(ev.screen)

        elif ev.type == MyEvTypes.PlSelectsMode:
            self._curr_texts = list(self._texts)
            self._curr_texts[ev.k] = MenuScreenView.tag_selected_mode(self._curr_texts[ev.k])
            self.refresh_labels()
