import sys

sys.path += ['../']

from Network import MyServer
from Network import Protocol

def AppServer(_Protocol):
    class _AppServer(MyServer.MyServer(_Protocol)):
        def __init__(self, port, keep_alive = -1):
            super(_AppServer, self).__init__(port, keep_alive)

            self.ls_action['CONNECT'] = self._connect
            self.ls_action['JUMP'] = self._jump
            self.ls_action['LEFT'] = self._left
            self.ls_action['RIGHT'] = self._right
            self.ls_action['BONUS'] = self._bonus
            self.ls_action['PLATFORM'] = self._platform

            self.ls_team = {}

        def _connect(self, sock, team, port):
            print 'New connection'

            if not team in self.ls_team:
                self.ls_team[team] = []

            s = _Protocol.Socket()
            s.connect(sock._handle.getpeername()[0], int(port))
            self.ls_team[team] += [s]

        def _jump(self, sock, team):
            print 'jump'

            if team in self.ls_team:
                for s in self.ls_team[team]:
                    self.add_message(s, "JUMP\r\n")

        def _left(self, sock, team):
            print 'left'

            if team in self.ls_team:
                for s in self.ls_team[team]:
                    self.add_message(s, "LEFT\r\n")

        def _right(self, sock, team):
            print 'right'

            if team in self.ls_team:
                for s in self.ls_team[team]:
                    self.add_message(s, "RIGHT\r\n")

        def _bonus(self, sock, team, num, x, y):
            print 'bonus'

            if team in self.ls_team:
                for s in self.ls_team[team]:
                    self.add_message(s, "BONUS " + num + " " + x + " " + y + "\r\n")

        def _platform(self, sock, team, x1, y1, x2, y2):
            print 'platform'

            if team in self.ls_team:
                for s in self.ls_team[team]:
                    self.add_message(s, "PLATFORM " + x1 + " " + y1 + " " + x2 + " " + y2 + "\r\n")

    return _AppServer

if __name__ == '__main__':
    server = AppServer(Protocol.TCP)(8080, -1)
    server.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.stop()
        server.join()

    sys.exit()


