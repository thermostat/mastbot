

class Actor(object):

    def __init__(self):
        pass

    def cares_about(self, note):
        return False

    def handle(self, note):
        return []




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

    
