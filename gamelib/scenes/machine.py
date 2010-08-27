"""Machine room where tools and machines are found."""

import random

from gamelib.state import Scene, Item, Thing, Result
from gamelib.cursor import CursorSprite
from gamelib.scenes.scene_widgets import (Door, InteractText, InteractNoImage,
                                          InteractRectUnion, InteractImage,
                                          InteractAnimated, GenericDescThing)


class Machine(Scene):

    FOLDER = "machine"
    BACKGROUND = "machine_room.png"

    INITIAL_DATA = {
        'accessible': True,
        }

    def __init__(self, state):
        super(Machine, self).__init__(state)
        self.add_thing(ToMap())
        self.add_thing(LaserWelder())
        self.add_thing(LaserWelderPowerLights())
        self.add_thing(Grinder())
        self.add_item(TitaniumMachete('machete'))
        self.add_item(TinPipe('tin_pipe'))
        self.add_thing(GenericDescThing('machine.wires', 2,
            "Wires run to all the machines in the room",
            (
                (250, 172, 252, 12),
                (388, 183, 114, 13),
                (496, 112, 36, 64),
                (533, 85, 19, 45),
                (647, 114, 10, 308),
                (111, 96, 13, 285),
                (152, 106, 34, 30),
                (189, 136, 27, 28),
                (222, 157, 24, 25),
                (120, 86, 34, 29),
                (110, 80, 21, 15),
                (383, 196, 12, 56),
                (553, 61, 26, 50),
                (574, 39, 16, 48),
                (648, 85, 22, 26),
                (674, 54, 23, 36),
                )))
        self.add_thing(GenericDescThing('machine.diagram', 3,
            "A wiring diagram of some sort",
            ((694, 140, 94, 185),)))
        self.add_thing(GenericDescThing('machine.powerpoint', 4,
            "The cables to this power point have been cut",
            ((155, 22, 92, 74),)))
        self.add_thing(GenericDescThing("machine.powerpoint", 5,
            "All the machines run off this powerpoint",
            ((593, 19, 74, 57),)))

    def enter(self):
        return Result("The machine room is dark and forbidding.")


class ToMap(Door):

    SCENE = "machine"

    INTERACTS = {
        "door": InteractNoImage(695, 350, 97, 212),
        }

    INITIAL = "door"

# welder.slot: 249, 324, 167, 51
# welder.button: 406, 389, 28, 31
# welder.power lights: 201, 278, 16, 170
# manual: 434, 496, 66, 34

# broken power socket: 160, 28, 68, 51
# working power socket: 587, 23, 82, 50
# poster: 706, 157, 76, 158

# drill press block: 461, 446, 38, 27
# drill press:
#Rect 0 :
#   (519, 338, 36, 63),
#   (545, 348, 93, 46),
#   (599, 309, 41, 150),
#   (588, 445, 66, 42),
#   (616, 479, 41, 14),
#   (527, 393, 15, 17),
#   (510, 360, 13, 11),
#   (532, 331, 14, 11),
#   (605, 304, 26, 8),

class LaserWelder(Thing):

    NAME = "machine.laser_welder"

    INTERACTS = {
        "weld": InteractNoImage(241, 310, 178, 66),
    }

    INITIAL = "weld"

    INITIAL_DATA = {
        'cans_in_place': 0,
    }

    def interact_without(self):
        if self.get_data('cans_in_place') < 1:
            return Result("The laser welder doesn't currently contain anything weldable.")
        elif self.get_data('cans_in_place') < 3:
            return Result("You'll need more cans than that.")
        else:
            self.set_data('cans_in_place', 0)
            self.state.add_inventory_item('tin_pipe')
            return Result("With high-precision spitzensparken, the cans are welded into a replacement tube.",
                    soundfile='laser.ogg')

    def interact_with_empty_can(self, item):
        starting_cans = self.get_data('cans_in_place')
        if starting_cans < 3:
            self.state.remove_inventory_item(item.name)
            self.set_data('cans_in_place', starting_cans + 1)
            return Result({
                    0: "You carefully place the empty can in the area marked 'to weld'.",
                    1: "You carefully place the empty can next to the other.",
                    2: "You carefully place the empty can next to its mates.",
                    }[starting_cans])
        else:
            return Result("The machine has enough cans to weld for the moment.")

    def get_description(self):
        if self.get_data('cans_in_place') == 0:
            return "This is a Smith and Wesson 'zOMG' class high-precision laser welder."
        msg = "The laser welder looks hungry, somehow."
        if self.get_data('cans_in_place') == 1:
            msg += " It currently contains an empty can."
        elif self.get_data('cans_in_place') == 2:
            msg += " It currently contains two empty cans."
        elif self.get_data('cans_in_place') == 3:
            msg += " It currently contains three empty cans."
        return msg


class LaserWelderPowerLights(Thing):

    NAME = "machine.welder.lights"

    INTERACTS = {
        "lights": InteractAnimated(199, 273, ["power_lights_%d.png" % i for i in range(8) + range(6,0,-1)], 10)
    }

    INITIAL = 'lights'

    def get_description(self):
        return random.choice([
            "The power lights pulse expectantly.",
            ])


class TinPipe(Item):
    "A pipe made out of welded-together tins."

    INVENTORY_IMAGE = "tube_fragments.png"
    CURSOR = CursorSprite('tube_fragments_cursor.png')
    TOOL_NAME = "pipe"


class Grinder(Thing):

    NAME = "machine.grinder"

    INTERACTS = {
        "grind": InteractNoImage(86, 402, 94, 63),
    }

    INITIAL = "grind"

    def interact_without(self):
        return Result("It looks like it eats fingers. Perhaps a different approach is in order?")

    def interact_with_titanium_leg(self, item):
        self.state.replace_inventory_item(item.name, 'machete')
        return Result("After much delicate grinding and a few close calls with"
                      " various body parts, the titanium femur now resembles"
                      " a machete more than a bone. Nice and sharp, too.",
                      soundfile="grinder.ogg")

    def get_description(self):
        return "A pretty ordinary, albeit rather industrial, grinding machine."


class TitaniumMachete(Item):
    "Titanium machete, formerly a leg."

    INVENTORY_IMAGE = "machete.png"
    CURSOR = CursorSprite('machete_cursor.png', 23, 1)


SCENES = [Machine]
