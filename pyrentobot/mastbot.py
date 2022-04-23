######################################################################
# Mastodon client
######################################################################

import mastodon
import os
import pprint
import random
import re
from bs4 import BeautifulSoup

from actor import Actor

class PyrentoMastBot(object):
    def __init__(self, since=None, cfg=None):
        self._mst = _mastbot_init()
        self._newest_id = since
        self._actors = []

    def mainloop(self):
        keep_going = True
        while keep_going:
            self.check_incoming()
            time.sleep(120)
            
    def check_incoming(self):
        newest_notes = mst.notifications(since_id=self._newest_id)
        if len(newest_notes):
            self._newest_id = newest_notes[0]['id']
            print("Most recent id: {}".format(self._newest_id))
        self._process_notifications(newest_notes)
        self._clear_notifications()


    def reply(self, status, msg):
        result = self._mst.status_post(msg, in_reply_to_id=status['status']['id'])

    def send_message(self, msg):
        result = self._mst.status_post(msg)
        

    def _mastbot_init(self):
        mst = mastodon.Mastodon(access_token=ACCESS_TOKEN, api_base_url='https://botsin.space/')
        return mst
        
    def _clear_notifications(self):
        self._mst.notifications_clear()


    def _process_notifications(self, notes):
        actions = []
        for note in notes:
            for actor in self._actors:
                if actor.cares_about(note):
                    actions.extend(actor.handle(note))
        for action in actions:
            self._execute(action)

    def _execute(self, action):
        action.execute(self)
                    
        
    def _xprocess_notifications(self, notes):
        for note in notes:
            if note['type'] == 'mention':
                print(fmt_status(note))
                txt = status_text(note)
                if txt.startswith("@pyrento_bot roll"):
                    x = re.search(r"(\d+)d(\d+)", txt)
                    if x:
                        sl = [int(y) for y in x.groups()]
                        rolls = [ random.randint(1, sl[1]) for x in range(sl[0]) ]
                        self.reply(note, "@{} {}".format(note['account']['username'],str(rolls)))



if __name__ == '__main__':
    print("ok")
