
import kivy
kivy.require('1.0.5')
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.popup import Popup

from Phidgets.PhidgetException import PhidgetException

from ltcbackend import LTCbackend

class LTCAccordionItem(AccordionItem):
    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        return super(AccordionItem, self).on_touch_down(touch)

class IgnitionPopup(Popup):
    def __init__(self, ignite, abort, **kwargs):
        self.ignite = ignite
        self.abort = abort
        super(IgnitionPopup, self).__init__(auto_dismiss=False, **kwargs)

    def ignitefunc(self):
        self.ignite()
# TODO: ignite 10 second timeout
class LTCctrl(Accordion):
    def __init__(self, ignite=lambda x: None, shorepower=lambda x: None, central_dict={}, **kwargs):
        super(LTCctrl, self).__init__(**kwargs)
        self.unarmed.collapse = False
        self.ignite = ignite
        self.shorepower = shorepower
        self.shorepower_button.state = 'normal'
        self.central_dict = central_dict

    def on_popup_ignite(self):
        try:
            self.ignite(True)
            self.central_dict['state'] = 'IGNITED!'
        except PhidgetException:
            self.abort()
            self.central_dict['state'] = 'Phidget Call Failed'

    def on_popup_abort(self):
        self.ignite_button.state = 'normal'

    def on_arm(self):
        if self.shorepower_button.state == 'down':
            self.armed.collapse = False
            self.central_dict['state'] = 'ARMED'

    def on_ignite(self):
        if self.ignite_button.state == 'normal':
            self.on_abort()
        else:
            IgnitionPopup(self.on_popup_ignite, self.on_popup_abort).open()

    def on_abort(self):
        try:
            self.ignite(False)
            if self.ignite_button.state == 'down':
                self.ignite_button.state = 'normal'
            self.unarmed.collapse = False
            self.central_dict['state'] = 'Nominal'
        except PhidgetException:
            self.central_dict['state'] = 'Phidget Call Failed'

    def on_shorepower(self, button, state):
        try:
            self.shorepower(state)
            button.state = 'down'
        except PhidgetException:
            button.state = 'normal'
            self.central_dict['state'] = 'Phidget Call Failed'


#########Module test########

import sys
from kivy.app import App
class ltcctrlApp(App):
    def build(self):
        try:
            if sys.argv[1] == '-t':
                cdict = dict()
                ltc = LTCbackend(cdict)
                return LTCctrl(ltc.ignite, ltc.shorepower)
            else:
                return LTCctrl()
        except IndexError:
            return LTCctrl()

if __name__ == '__main__':
    ltcctrlApp().run()
