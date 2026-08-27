# import socket module
import sys
import threading
from dataclasses import dataclass
from pathlib import Path
from socket import *

from logger.logger import getLogger

from . import connection

serverSocket = socket(AF_INET, SOCK_STREAM)
localStorage = (
    Path(__file__).parent.parent / "public"
)  # this might look like "magic", but it is just hte path of the public dir


log = getLogger(__name__)


# this is the start of the server listener
def start(host: str, port: int):
    # configuring the server with the vars and starting it
    serverSocket.bind((host, port))
    serverSocket.listen(1)
    log.info(f"server started. listening on port {port}")

    # listening loop here
    while True:
        # Establish the connection
        connectionSocket, addr = serverSocket.accept()

        # dispatch a new thread to handle the connection request
        threading.Thread(
            target=connection.dispatch,
            args=(connectionSocket, localStorage),
            # passing localStorage to the handler thread because it seems more natural to define in one place and pass downstream
        ).start()


def shutdown(signum, frame):
    log.info(f"\nstarting graceful shutdown.")
    serverSocket.close()
    log.info("server shutdown successfully. bye!")
    sys.exit(0)
