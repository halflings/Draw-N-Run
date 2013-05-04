import threading
import math

import Server
import Protocol

def MyServer(_Protocol):
    '''Generateur d'une meta-class de serveur en fonction du parametre utilise.'''

    class _MyServer(Server.Server(_Protocol)):
        '''Serveur associant une action a faire pour une requete de la forme MOT ARG1 ARGS2 ...\r\n.'''

        def __init__(self, port, keep_alive = -1):
            '''Initialisation du serveur et association des actions de bases.

            Parametre:
                port       -- port d'ecoute du serveur
                keep_alive -- temps max d'inactivite d'un socket
            '''

            super(_MyServer, self).__init__(port, keep_alive)

            self.ls_action = {}

            self.ls_action['END'] = self._end

            self.ls_message = []

        def accept_client(self, client):
            '''Fonction d'acceptation des clients.

            Parametre:
                client -- socket de connexion au client
            '''

            return _Protocol == Protocol.TCP

        def parse(self, sock, msg):
            '''Decoupe le message en ligne et l'analyse. Si pour une ligne, le premier mot est une action valide, alors la fonction associe est appele avec les parametres transmis.

            Parametre:
                sock -- socket ayant envoyer le message
                msg  -- message envoye
            '''

            lines = [l.strip() for l in msg.split('\r\n') if l.strip()]
            for l in lines:
                words = [w.strip() for w in l.split(' ') if w.strip()]

                if len(words) > 0:
                    if words[0] in self.ls_action:
                        f = self.ls_action[words[0]]
                        args = tuple([sock] + words[1:])
                        f(*args)

        def _end(self, sock):
            '''Fonction de fin de la communication

            Parametre:
                sock -- client ayant demande la fin de la communication.
            '''

            self.disconnect(sock)

    return _MyServer

