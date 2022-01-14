import tempfile
import os
import fcntl
import socket
from multiprocessing.managers import BaseManager
import hashlib


class ApplicationContextManager(BaseManager): pass


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


class ContextServer(object):

    def __init__(self, server_name, port: int = 5000, function=None, password: str = None):
        self.server_name = server_name
        self.port = port
        self.password = password
        self.function = function
        self.server_file = os.path.join(tempfile.gettempdir(), self.server_name + ".server")
        self.APPLICATION_CONTEXT = None

    def run(self):
        print("A")
        if self.__try_lock():
            print("B")
            self.__make_context()
            return
        print("C")
        self.__load_context()

    def __load_context(self):
        ApplicationContextManager.register('get_application_context')
        manager = ApplicationContextManager(
            address=('localhost', self.port),
            authkey=bytes(
                self.get_auth_key() if not self.password else self.password,
                encoding='utf-8'
            )
        )
        manager.connect()
        self.APPLICATION_CONTEXT = manager.get_application_context()._getvalue()
        print(":-?")

    def get_application_context(self):
        return self.APPLICATION_CONTEXT

    def __make_context(self):
        self.APPLICATION_CONTEXT = dict()
        ApplicationContextManager.register('get_application_context', self.get_application_context)
        manager = ApplicationContextManager(
            address=('localhost', self.port),
            authkey=bytes(
                self.get_auth_key() if not self.password else self.password,
                encoding='utf-8'
            )
        )
        self.__lock_file()
        if self.function:
            self.function(self.APPLICATION_CONTEXT)
        server = manager.get_server()
        server.serve_forever()

    def __try_lock(self):
        try:
            fh = open(self.server_file, 'r')
            return False
        except:
            # if file does not exist, create it
            fh = open(self.server_file, 'w')
            fh.close()
            return True

    def __lock_file(self):
        fp = open(self.server_file, 'w')
        try:
            fcntl.flock(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
            success = True
        except IOError:
            success = False
        fp.close()
        return success

    def get_auth_key(self) -> str:
        return hashlib.sha1(self.server_name.encode('utf-8')).hexdigest()
