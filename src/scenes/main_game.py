import pygame

from src import constants
from src.scenes.scene import Scene, DevOverlay
from src.helpers import main_to_small_display
from src.world import World
from src import enemy


class MainGame(Scene):
    def __init__(self, game, world_name):
        super().__init__(game, MainGameDevOverlay)
        self.world = World(world_name)
        # self.enemies = []
        self.mouse_pos_world = pygame.Vector2()
        self.mouse_rel = pygame.Vector2()
        self.mouse_dy = tuple(enumerate((constants.PLATFORM_HEIGHT, 0)))
        self.tile_at_mouse = None

    def start(self):
        super().start()

    def process_event(self, event, event_manager):
        block = super().process_event(event, event_manager)
        if block:
            return True
        if event.type == pygame.KEYDOWN:
            if event.key == event_manager.k_escape:
                self.pause()
                return True
            # elif event.key == self.event_manager.k_next_wave:
            #     self.next_wave()
            elif event.key == event_manager.k_scroll_left:
                self.world.scroll_direction.x -= 1
            elif event.key == event_manager.k_scroll_right:
                self.world.scroll_direction.x += 1
            elif event.key == event_manager.k_scroll_up:
                self.world.scroll_direction.y -= 1
            elif event.key == event_manager.k_scroll_down:
                self.world.scroll_direction.y += 1
        elif event.type == pygame.KEYUP:
            if event.key == event_manager.k_scroll_left:
                self.world.scroll_direction.x += 1
            elif event.key == event_manager.k_scroll_right:
                self.world.scroll_direction.x -= 1
            elif event.key == event_manager.k_scroll_up:
                self.world.scroll_direction.y += 1
            elif event.key == event_manager.k_scroll_down:
                self.world.scroll_direction.y -= 1
        elif (event.type == pygame.MOUSEMOTION
              and event.buttons[event_manager.mouse_map_scroll_button_index]):
            self.mouse_rel.update(main_to_small_display(*event.rel))
            self.world.scroll(self.mouse_rel)

    def update(self, dt):
        super().update(dt)
        self.mouse_pos_world.update(
            self.world.small_display_to_world_pos(*self.mouse_pos)
        )
        self.world.update(dt)
        self.get_tile_at_mouse()
        self.highlight_tile_at_mouse()
        # for e in self.enemies:
        #     e.update(dt)

    def draw(self):
        self.target_surface.fill((0, 0, 0))
        self.world.draw(self.target_surface)

        # for e in self.enemies:
        #     target_surface.blit(
        #         e.image,
        #         world_to_screen(
        #             e.rect.x, e.rect.y,
        #             0, e.offset_y,
        #             self.camera_offset_x, self.camera_offset_y
        #         )
        #     )

    def get_tile_at_mouse(self):
        # I want to detect a platform only when the mouse is over the raised
        # part. The sides and base don't matter. I hope this will simplify
        # snapping the towers to the platforms.
        tiles = [None, None]
        for i, dy in self.mouse_dy:
            tile_pos_x, tile_pos_y = self.world.small_display_to_tile_pos(
                self.mouse_pos.x,
                self.mouse_pos.y + dy
            )
            tiles[i] = self.world.get_tile_at(tile_pos_x, tile_pos_y)
        if tiles[0] is not None and tiles[0].type == "platform":
            self.tile_at_mouse = tiles[0]
        elif tiles[1] is not None and tiles[1].type == "path":
            self.tile_at_mouse = tiles[1]
        else:
            self.tile_at_mouse = None

    def highlight_tile_at_mouse(self):
        if self.tile_at_mouse is None:
            self.world.highlight.layer = -1
            return
        self.world.highlight.layer = 1
        self.world.highlight.world_pos.update(self.tile_at_mouse.world_pos)
        self.world.highlight.surface_pos.update(self.tile_at_mouse.surface_pos)

    def pause(self):
        self.close("pause menu",remove_self=False)

    # def next_wave(self):
    #     self.enemies.append(Enemy("cube", self.world.path))


class MainGameDevOverlay(DevOverlay):
    def __init__(self, scene):
        super().__init__(scene)

        self.tile_info_text = ""
        self.tile_info_surf = None
        self.tile_info_rect = None

        self.mouse_pos_text = ""
        self.mouse_pos_surf = None
        self.mouse_pos_rect = None

    def update(self, clock):
        super().update(clock)

        if self.scene.tile_at_mouse is None:
            new_tile_info_text = "tile at mouse: none"
        else:
            new_tile_info_text = (
                f"tile at mouse: {self.scene.tile_at_mouse.type}" +
                f" ({self.scene.tile_at_mouse.world_pos.x:.0f}, " +
                f"{self.scene.tile_at_mouse.world_pos.y:.0f})"
            )
        if new_tile_info_text != self.tile_info_text:
            self.tile_info_text = new_tile_info_text
            self.tile_info_surf, self.tile_info_rect = self.dev_font.render(
                self.tile_info_text
            )
            self.tile_info_rect.topleft = (self.dev_margin.x, self.dev_margin.y * 3)

        x, y = self.scene.mouse_pos_world
        new_mouse_pos_text = f"mouse position in world: ({x:.1f}, {y:.1f})"
        if new_mouse_pos_text != self.mouse_pos_text:
            self.mouse_pos_text = new_mouse_pos_text
            self.mouse_pos_surf, self.mouse_pos_rect = self.dev_font.render(
                self.mouse_pos_text
            )
            self.mouse_pos_rect.topleft = (self.dev_margin.x, self.dev_margin.y * 5)

    def draw(self):
        super().draw()

        self.target_surface.blit(self.tile_info_surf, self.tile_info_rect)
        self.target_surface.blit(self.mouse_pos_surf, self.mouse_pos_rect)

        pygame.draw.rect(
            self.target_surface,
            constants.DEV_COLOR,
            pygame.Rect([r * constants.MAGNIFICATION for r in self.scene.world.rect]),
            1
        )
