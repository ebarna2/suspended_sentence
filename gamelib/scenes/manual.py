"""The inside of the maintenance manual."""

from pyntnclick.state import Scene, Thing
from pyntnclick.scenewidgets import InteractNoImage, InteractImage


# classes related the computer detail


class PageBase(Thing):
    "Displays manual pages"

    def get_page_thing(self):
        return self.scene.things['manual.page']

    def get_page(self):
        return self.get_page_thing().get_data('page')

    def set_page(self, page):
        self.get_page_thing().set_page(page)

    def select_interact(self):
        return self.get_data('display')

    def set_display(self, display):
        self.set_data('display', display)
        self.set_interact()

    def is_interactive(self, tool=None):
        return self.get_data('display') == 'on'


class PagePrior(PageBase):
    """Prior page in the manual"""

    NAME = 'manual.page_prior'

    INTERACTS = {
            'on': InteractImage(36, 351, 'arrow_left.png'),
            'off': InteractNoImage(31, 351, 34, 23),
            }
    INITIAL = 'off'

    INITIAL_DATA = {
        'display': 'off',
        }

    def interact_without(self):
        self.set_page(self.get_page() - 1)


class PageNext(PageBase):
    """Next page in the manual"""

    NAME = 'manual.page_next'

    INTERACTS = {
            'on': InteractImage(185, 351, 'arrow_right.png'),
            'off': InteractNoImage(185, 351, 34, 23),
            }
    INITIAL = 'on'

    INITIAL_DATA = {
        'display': 'on',
        }

    def interact_without(self):
        self.set_page(self.get_page() + 1)


class ManualPage(Thing):
    """Page in the manual"""

    NAME = 'manual.page'

    INTERACTS = {
            0: InteractImage(0, 0, 'manual_p1.png'),
            1: InteractImage(0, 0, 'manual_p2.png'),
            2: InteractImage(0, 0, 'manual_p3.png'),
            3: InteractImage(0, 0, 'manual_p4.png'),
            }
    INITIAL = 0

    INITIAL_DATA = {
        'page': 0,
        }

    def is_interactive(self, tool=None):
        return False

    def select_interact(self):
        return self.get_data('page')

    def set_page(self, page):
        self.set_data('page', page)
        self.set_interact()
        self.scene.things['manual.page_prior'].set_display('on')
        self.scene.things['manual.page_next'].set_display('on')
        if page == 0:
            self.scene.things['manual.page_prior'].set_display('off')
        if page == len(self.INTERACTS) - 1:
            self.scene.things['manual.page_next'].set_display('off')


class ManualDetail(Scene):

    FOLDER = 'manual'
    NAME = 'manual_detail'

    BACKGROUND = 'manual_detail.png'

    def setup(self):
        self.add_thing(ManualPage())
        self.add_thing(PagePrior())
        self.add_thing(PageNext())
        self._scene_playlist = None

    def enter(self):
        self._scene_playlist = self.sound.get_current_playlist()
        self.sound.change_playlist(None)

    def leave(self):
        self.sound.change_playlist(self._scene_playlist)


SCENES = []
DETAIL_VIEWS = [ManualDetail]
