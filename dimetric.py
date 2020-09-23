"""Run this file to run the game."""

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


import os
# Must be done before importing Pygame:
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
os.environ["SDL_VIDEO_CENTERED"] = "1"

import pygame

from src import constants
from src import resources
from src import states
from src.event_manager import EventManager


class Game:
    def __init__(self, initial_state_name):
        pygame.init()
        self.main_display = pygame.display.set_mode(constants.MAIN_DISPLAY_SIZE)
        self.small_display = pygame.Surface(constants.SMALL_DISPLAY_SIZE)
        resources.load_all()
        self.running = True
        self.states = {
            "main menu": states.MainMenu,
            "options menu": states.OptionsMenu,
            "main game": states.MainGame
        }
        self.state = self.states[initial_state_name]()

    def change_states(self):
        # TODO: Some states must be interruptible without losing data. E.G. the
        #  main game instance should continue after pausing without creating
        #  a new instance. Maybe just put a pointer to it into the persistent
        #  data. Or save it in here.
        persistent_state_data = self.state.persistent_state_data
        next_state_name = persistent_state_data["next_state_name"]
        if next_state_name == "quit":
            # TODO: If there are unsaved changes, ask if they should be
            #  saved, discarded or if the exit should be canceled. That
            #  popup will be its own state. And that one may exit the game.
            self.running = False
        elif next_state_name == "main game":
            world_name = persistent_state_data["world_name"]
            self.state = self.states[next_state_name](world_name)
        else:
            self.state = self.states[next_state_name]()
        self.state.resume(persistent_state_data)

    def run(self):
        event_manager = EventManager()
        clock = pygame.time.Clock()

        while self.running:
            # delta time of previous tick in seconds. Protect against hiccups
            # (e.g. from moving the pygame window) by limiting to 0.1 s.
            dt = min(clock.tick(constants.FPS) / 1000, 0.1)

            if self.state.is_done:
                self.change_states()

            event_manager.process_events(self.state)
            self.state.update(dt)

            self.state.draw(self.small_display)
            pygame.transform.scale(
                self.small_display,
                constants.MAIN_DISPLAY_SIZE,
                self.main_display
            )
            if self.state.dev_overlay_visible:
                self.state.draw_dev_overlay(self.main_display, clock)
            pygame.display.flip()


if __name__ == "__main__":
    game = Game("main menu")
    game.run()
