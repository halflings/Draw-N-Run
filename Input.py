import threading

from Network import Server
from Network import Protocol

def InputServer(_Protocol):
    class _InputServer(Server.BasicServer):
        def __init__(self, team, addr, port, keep_alive):
            super(_InputServer, self).__init__(keep_alive)

            self.team = team

            self.sout = _Protocol.Socket()
            self.sout.connect(addr, port)
            self.outputs += [self.sout]
            self.always_alive += [self.sout]

        def jump(self):
            self.add_message(self.sout, "JUMP " + str(self.team) + "\r\n")

        def left(self):
            self.add_message(self.sout, "LEFT " + str(self.team) + "\r\n")

        def right(self):
            self.add_message(self.sout, "RIGHT " + str(self.team) + "\r\n")

        def bonus(self, num, p):
            self.add_message(self.sout, "BONUS " + str(self.team) + " " + str(num) + " " + str(p[0]) + " " + str(p[1]) + "\r\n")

        def platform(self, p1, p2):
            self.add_message(self.sout, "PLATFORM " + str(self.team) + " " + str(p1[0]) + " " + str(p1[1]) + " " + str(p2[0]) + " " + str(p2[1]) + "\r\n")

        def end(self):
            self.add_message(self.sout, "END\r\n")

    return _InputServer

