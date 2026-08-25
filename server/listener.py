# import socket module
import sys
import threading
from dataclasses import dataclass
from pathlib import Path
from socket import *

from . import connection

serverSocket = socket(AF_INET, SOCK_STREAM)
localStorage = (
    Path(__file__).parent.parent / "public"
)  # looks magic, but just finds script path than go to storage dir


def start(host: str, port: int):
    # configuring the server with the vars and starting it
    serverSocket.bind((host, port))
    serverSocket.listen(1)
    print(f"server started. listening on port {port}")

    # listening loop
    while True:
        # Establish the connection
        connectionSocket, addr = serverSocket.accept()

        # dispatch a new thread to handle the connection request
        threading.Thread(
            target=connection.dispatch,
            args=(connectionSocket, localStorage),
        ).start()


def shutdown(signum, frame):
    print(f"\nstarting graceful shutdown.")
    serverSocket.close()
    print("server shutdown successfully. bye!")
    sys.exit(0)
