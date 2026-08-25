import time
from socket import socket, timeout

from .messages import HTTPRequest, HTTPResponse


def receiveRequest(connectionSocket: socket) -> HTTPRequest:
    headerBytes = _readHTTPHeaderBytes(connectionSocket=connectionSocket)
    method, path, version, header = _parseRequestHeader(headerBytes)
    body = ""

    length = header.get("Content-Length", None)
    if length:
        bodyBytes = _readHTTPBodyBytes(
            connectionSocket=connectionSocket, length=int(length)
        )
        body = parseRequestBody(bodyBytes)

    return HTTPRequest(
        method=method, path=path, http_version=version, header=header, body=body
    )


def _readHTTPHeaderBytes(connectionSocket: socket) -> bytes:
    # for simplicity, first read the header, then parse it, then take the Content-Length in header, then read the next bytes, which is the body
    req = b""
    # will add 5.0s of timeout with a monotonic clock, since while can go forever if client disconnects midway
    loopTimeout = 5.0  # 5s of timoeut
    start_time = time.monotonic()
    while b"\r\n\r\n" not in req and (time.monotonic() < start_time + loopTimeout):
        req += connectionSocket.recv(1)

    return req


def _parseRequestHeader(req: bytes):
    decoded_req = req.decode()

    msg = [i for i in decoded_req.split("\r\n")]

    # start line
    method, path, version = msg[0].split(" ")

    # header
    header = dict[str, str]()
    i = 1
    while msg[i] != "":
        sla = msg[
            i
        ].split(
            ":", 1
        )  # splits on just the first ":", got some problems with it from browser html requests...
        print(sla)
        k, v = sla
        header[k] = v
        i += 1

    return method, path, version, header


def _readHTTPBodyBytes(connectionSocket: socket, length: int) -> bytes:
    req = b""

    # add some timeout to the loop again
    loopTimeout = 5.0  # 5s of timoeut
    start_time = time.monotonic()
    i = 0
    while i < length and (time.monotonic() < start_time + loopTimeout):
        req += connectionSocket.recv(1)
    return req


def parseRequestBody(req: bytes):
    return req.decode()


def generateResponse(res: HTTPResponse):
    headerStr = ""
    for k, v in res.header.items():
        headerStr += f"{k.removesuffix(':')}: {v}\r\n"
    serializedResponse = f"HTTP/1.1 {res.status} {res.reason}\r\n{headerStr}\r\n"
    if res.body:
        serializedResponse += res.body

    return serializedResponse.encode("utf-8")
