import datetime
OUTGOING = 2
INCOMING_READ = 1
INCOMING_UNREAD = 0
class Telegram():
    def __init__(self, username, localID, message, timestamp, telegramType):
        self.username = username
        self.localID = localID
        self.message = message
        self.timestamp = timestamp
        self.date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y/%m/%d')
        self.time = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
        self.type = telegramType
    def MakeText(self):
        if self.message.startswith('\x0A\x01'):
            message = 'Friend request from ' + self.message[2:].strip()
        else:
            message = self.message
        if self.type == OUTGOING:
            return f'Type: Outgoing\tFrom: ({self.localID})\tTo: {self.username}\tDate: {self.date} {self.time}\tMessage: {message}'
        elif self.type == INCOMING_READ:
            return f'Type: Incoming, read\tFrom: {self.username}\tTo: ({self.localID})\tDate: {self.date} {self.time}\tMessage: {message}'
        elif self.type == INCOMING_UNREAD:
            return f'Type: Incoming, unread\tFrom: {self.username}\tTo: ({self.localID})\tDate: {self.date} {self.time}\tMessage: {message}'
        else:
            return ''
    def MakeCSV(self):
        if self.message.startswith('\x0A\x01'):
            message = 'Friend request from ' + self.message[2:].strip()
        else:
            message = self.message
        if self.type == OUTGOING:
            return f'"Outgoing","({self.localID})","{self.username}","{self.date} {self.time}","{message}"'
        elif self.type == INCOMING_READ:
            return f'"Incoming, read","{self.username}","({self.localID})","{self.date} {self.time}","{message}"'
        elif self.type == INCOMING_UNREAD:
            return f'"Incoming, unread","{self.username}","({self.localID})","{self.date} {self.time}","{message}"'
        else:
            return ''
            

def OutputText(telegrams):
    lines = []
    for telegram in sorted(telegrams, key=lambda x: x.timestamp):
        lines.append(telegram.MakeText())
    return '\n'.join(lines)

def OutputCSV(telegrams):
    lines = []
    lines.append('Type, From, To, Date, Message')
    for telegram in sorted(telegrams, key=lambda x: x.timestamp):
        lines.append(telegram.MakeCSV())
    return '\n'.join(lines)
        
