import logging

import pygame
import pygame.freetype

from src import constants
from src import resources
from src.scenes import SCENES
from src.event_manager import EventManager


class Game:
    def __init__(self, initial_scene_name):
        pygame.init()
        self.main_display = pygame.display.set_mode(constants.MAIN_DISPLAY_SIZE)
        self.small_display = pygame.Surface(constants.SMALL_DISPLAY_SIZE)
        resources.load_all()
        self.running = True
        self.active_scenes = []
        self.active_scenes_reversed = []
        # Only the dev overlay of the front scene may be active and visible.
        self.active_dev_overlay = None
        self.dev_overlay_visible = True
        self.persistent_scene_data = {}
        self.change_scenes([], new_scene_name=initial_scene_name)

    def change_scenes(self, remove, new_scene_name=""):
        logging.debug(
            "Scene change. new = \"%s\", remove = %s.",
            new_scene_name,
            remove
        )
        for r in remove:
            self.active_scenes.remove(r)
        if not new_scene_name:
            if not self.active_scenes:
                print(new_scene_name)
                self.quit()
        else:
            if new_scene_name == "main game":
                world_name = self.persistent_scene_data["world name"]
                new_scene = SCENES[new_scene_name](self, world_name)
                self.active_scenes.append(new_scene)
            else:
                new_scene = SCENES[new_scene_name](self)
                self.active_scenes.append(new_scene)
            new_scene.start()
        if self.active_scenes:
            self.active_scenes_reversed = list(reversed(self.active_scenes))
            self.active_dev_overlay = self.active_scenes[-1].dev_overlay
        logging.debug("New active scenes: %s", self.active_scenes)

    def quit(self):
        # TODO: If there are unsaved changes, ask if they should be
        #  saved, discarded or if the exit should be canceled. That
        #  popup will be its own scene. And that one may then exit the game.
        self.running = False

    def run(self):
        event_manager = EventManager()
        clock = pygame.time.Clock()
        logging.info("Begin main loop.")
        while self.running:
            # delta time of previous tick in seconds.
            # Protect against hiccups (e.g. from moving the pygame window)
            # by limiting to 100 milliseconds.
            dt = min(clock.tick(constants.FPS), 100) / 1000

            for event in pygame.event.get():
                # process events front to back
                for scene in self.active_scenes_reversed:
                    if scene.process_event(event, event_manager) is not None:
                        break

            # update front to back
            for scene in self.active_scenes_reversed:
                if scene.update(dt) is not None:
                    break

            # draw back to front
            for scene in self.active_scenes:
                scene.draw()

            pygame.transform.scale(
                self.small_display,
                constants.MAIN_DISPLAY_SIZE,
                self.main_display
            )
            if self.dev_overlay_visible:
                self.active_dev_overlay.update(clock)
                self.active_dev_overlay.draw()
            pygame.display.flip()
        logging.info("End main loop.")
