# Copyright (C) 2020  Sebastian Henz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import pygame

from src import constants
from src.states.state import State
from src import button


class MainMenu(State):
    def __init__(self, game):
        super().__init__(game)

        self.buttons = (
            button.Button(
                "New Game",
                (100, 50),
                (constants.SMALL_DISPLAY_WIDTH // 2, 50),
                self.new_game
            ),
            button.Button(
                "Options",
                (100, 50),
                (constants.SMALL_DISPLAY_WIDTH // 2, constants.SMALL_DISPLAY_HEIGHT // 2),
                self.goto_options
            ),
            button.Button(
                "Quit",
                (100, 50),
                (constants.SMALL_DISPLAY_WIDTH // 2, 200),
                self.close
            )
        )

    def process_event(self, event, event_manager):
        super().process_event(event, event_manager)
        if event.type == pygame.KEYDOWN:
            if event.key == event_manager.k_escape:
                self.close()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event_manager.adjust_mouse(*event.pos)
            for b in self.buttons:
                if b.rect.collidepoint(x, y):
                    b.action()
                    break

    def update(self, dt):
        for b in self.buttons:
            b.update(self.mouse_pos)

    def draw(self, target_surface):
        target_surface.fill((0, 0, 0))
        for b in self.buttons:
            target_surface.blit(b.image, b.rect)

    def new_game(self):
        self.persistent_state_data["world_name"] = "test"
        self.close("main game")

    def goto_options(self):
        self.close("options menu")
