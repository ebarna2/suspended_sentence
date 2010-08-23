import unittest

import pygame

from gamelib import state

from pygame.locals import SWSURFACE
from gamelib.constants import SCREEN


# We need this stuff set up so we can load images and whatnot.
pygame.display.init()
pygame.display.set_mode(SCREEN, SWSURFACE)


class GameLogicTestCase(unittest.TestCase):
    CURRENT_SCENE = None

    def setUp(self):
        self.state = state.initial_state()
        self.state.set_current_scene(self.CURRENT_SCENE)

    def set_game_data(self, key, value, thing=None, scene=None):
        if scene is None:
            scene = self.CURRENT_SCENE
        gizmo = self.state.scenes[scene]
        if thing is not None:
            gizmo = gizmo.things[thing]
        gizmo.set_data(key, value)

    def assert_game_data(self, key, value, thing=None, scene=None):
        if scene is None:
            scene = self.CURRENT_SCENE
        gizmo = self.state.scenes[scene]
        if thing is not None:
            gizmo = gizmo.things[thing]
        self.assertEquals(value, gizmo.get_data(key))

    def assert_inventory_item(self, item, in_inventory=True):
        self.assertEquals(in_inventory, self.state.items[item] in self.state.inventory)

    def interact_thing(self, thing, item=None):
        item_obj = None
        if item is not None:
            item_obj = self.state.items[item]
        self.state.scenes[self.CURRENT_SCENE].things[thing].interact(item_obj)
