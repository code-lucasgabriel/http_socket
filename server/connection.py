from pathlib import Path
from socket import socket

from httpcore import wire
from logger.logger import getLogger

from . import handler

log = getLogger(__name__)


def dispatch(connectionSocket: socket, localStorage: Path):
    connectionSocket.settimeout(5.0)

    try:
        # call parser to parse the http request and feed the data type
        httpReq = wire.receiveRequest(connectionSocket=connectionSocket)

        # call handler so it generate a response msg
        httpRes = handler.handle(req=httpReq, localStorage=localStorage)
        resBytes = wire.generateResponse(httpRes)

        _ = connectionSocket.send(resBytes)
        connectionSocket.close()
    except Exception as e:
        # log exceptino, and respond client with bad request
        log.exception("an error occurred")

        resBytes = wire.generateResponse(handler.badRequest())
        _ = connectionSocket.send(resBytes)

        connectionSocket.close()
