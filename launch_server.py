import sys
from Network import Protocol, Server
s = Server.Server(Protocol.TCP)(8080, -1)
s.start()
try:
    while True:
        pass
except KeyboardInterrupt:
    s.stop()
    s.join()

sys.exit()
