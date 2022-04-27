
import mastodon
import os
import pprint
import random
import re
from bs4 import BeautifulSoup


ACCESS_TOKEN=os.environ['MASTBOT_ACCESS_TOKEN']
mst = None

def mastbot_init():
    global mst
    mst = mastodon.Mastodon(access_token=ACCESS_TOKEN, api_base_url='https://botsin.space/')
    return mst


def say_something(txt):
    return mst.toot(txt)

def incoming_msg():
    incoming = mst.notifications()
    pprint.pprint(incoming)

def status_text(status):
    return BeautifulSoup(status["status"]["content"], features='html.parser').get_text()

def fmt_status(status):
    return "{name}: {text}".format(name=status['account']['display_name'],
                                   text=status_text(status))

class PyrentoBot(object):
    def __init__(self, since=None, cfg=None):
        self._mst = mastbot_init()
        self._newest_id = since
    

    def check_incoming(self):
        newest_notes = mst.notifications(since_id=self._newest_id)
        if len(newest_notes):
            self._newest_id = newest_notes[0]['id']
            print("Most recent id: {}".format(self._newest_id))
        self._process_notifications(newest_notes)
        self._clear_notifications()


    def _reply(self, status, msg):
        print("sending {}".format(msg))
        result = self._mst.status_post(msg, in_reply_to_id=status['status']['id'])
        pprint.pprint(status)
        print(status['status']['id'])
        print(result)

    def _clear_notifications(self):
        self._mst.notifications_clear()
        
    def _process_notifications(self, notes):
        for note in notes:
            if note['type'] == 'mention':
                print(fmt_status(note))
                txt = status_text(note)
                if txt.startswith("@pyrento_bot roll"):
                    x = re.search(r"(\d+)d(\d+)", txt)
                    if x:
                        sl = [int(y) for y in x.groups()]
                        rolls = [ random.randint(1, sl[1]) for x in range(sl[0]) ]
                        self._reply(note, "@{} {}".format(note['account']['username'],str(rolls)))



                        
if __name__ == '__main__':
    import sys
    #mastbot_init()
    #print(say_something(sys.argv[1]))
    #incoming_msg()
    since = 4722528
    pb = PyrentoBot(since)
    pb.check_incoming()
    
    
