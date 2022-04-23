
from bs4 import BeautifulSoup
import re, random

class Actor(object):

    def __init__(self):
        pass

    def _html2txt(self, html):
        return BeautifulSoup(html, features='html.parser').get_text()
    
    def cares_about(self, note):
        note_txt = self._html2txt(note["status"]["content"])
        return self._cares_txt(note_txt)

    def _cares_txt(self, txt):
        return False

    def handle(self, note):
        note_txt = self._html2txt(note["status"]["content"])
        return self._handle_txt(note_txt, note)

    def _handle_txt(self, note_txt, note):
        return []


class RollActor(Actor):

    def _cares_txt(self, txt):
        return txt.startswith("@pyrento_bot roll")

    def _roll(self, txt):
        re_s = re.search(r"(\d+)d(\d+)(\+\d+)?", txt)
        roll_txt = ""
        if re_s:
            sl = [int(y) for y in re_s.groups() if y]
            rolls = [ random.randint(1, sl[1]) for re_s in range(sl[0]) ]
            add = 0
            if len(sl) > 2:
                add = sl[2]
            roll_txt = "{} : {}".format(sum(rolls)+add, str(rolls))
        return roll_txt
        

    def _handle_txt(self, txt, note):
        result = []
        try:
            roll_txt = self._roll(txt)
            if roll_txt:
                result.append(SendMessage("@{} {}".format(note['account']['username'],roll_txt),
                                          reply_id=note['status']['id']) )
        except Exception:
            print("RollActor Exception")
        return result

                

class Action(object):

    def execute(self, bot):
        pass


class SendMessage(Action):

    def __init__(self, msg, reply_id=None):
        self._msg = msg
        self._reply_id = reply_id


    def execute(self, bot):
        if self._reply_id:
            bot.reply(self._msg, self._reply_id)
        else:
            bot.send_message(self._msg)

    
