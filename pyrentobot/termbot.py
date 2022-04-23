

import mastbot
import actor

def mknote(msg):
    result = {}
    result['type'] = 'mention'
    result['account'] = {}
    result['account']['username'] = 'cliuser'
    result['id'] = 0
    result['status'] = {}
    result['status']['content'] = msg
    result['status']['id'] = 0
    return result


class TermBot(mastbot.BaseBot):
    def __init__(self, cfg):
        super(TermBot, self).__init__()
        self._cfg = cfg


    def reply(self, status, msg):
        print(msg)

    def send_message(self, msg):
        print(msg)

    def check_incoming(self):
        note = input("> ")
        notes = [mknote(note)]
        self._process_notifications(notes)


if __name__ == '__main__':
    tb = TermBot({})
    tb._actors.append(actor.RollActor())
    tb.mainloop()
