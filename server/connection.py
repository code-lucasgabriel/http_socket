from pathlib import Path
from socket import socket

from httpcore import wire

from . import handler


def dispatch(connectionSocket: socket, localStorage: Path):
    try:
        httpReq = wire.receiveRequest(connectionSocket=connectionSocket)

        # call parser to parse the http request and feed the data type

        # call handler so it generate a response msg
        httpRes = handler.handle(req=httpReq, localStorage=localStorage)
        resBytes = wire.generateResponse(httpRes)

        _ = connectionSocket.send(resBytes)
        connectionSocket.close()
    except:
        print("some error occurred!")
        connectionSocket.close()
