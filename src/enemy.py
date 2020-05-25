"""Enemies."""

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

from src.resources import sprites
from src.coordinate_conversion import map_to_screen


class Enemy:
    def __init__(self, enemy_type, path):
        self.type = enemy_type
        self.path = path
        self.surface = sprites[self.type]

        # FIXME: Achtung, ich muss hier unterscheiden zwischen width und height
        #  in map space und screen space! Das Rect ist für Kollisionen im
        #  map space gedacht. Das heißt ich muss sehr genau aufpassen, wie ich
        #  die Sachen benennen und zwischen map und screen umrechne.

        width, height = self.surface.get_size()
        height_dimetric = width // 2
        self.offset_y = height_dimetric - height
        # Rect in map space, used for collision detection, not for blitting.
        self.rect = pygame.Rect(-1, -1, width, height_dimetric)
        print(self.rect)
        self.rect.center = path[0]

        self.hitpoints = 100
        self.speed = 1
        self.direction = [1, 0]  # [x, y]

        print(path[0])
        print(self.rect.center)
        print(self.rect)

    def update(self, dt):
        pass