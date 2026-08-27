from pathlib import Path

from httpcore.messages import HTTPRequest, HTTPResponse
from logger.logger import getLogger
from storage import filestore

log = getLogger(__name__)


def handle(req: HTTPRequest, localStorage: Path) -> HTTPResponse:
    # this method receives a request, than decides which response to give
    # pretty simple, is just a conditional router
    # btw it just supports GET method for now
    match req.method:
        case "GET":
            fileName = req.path.removeprefix("/")
            content, ok = filestore.find(
                localStorage,
                fileName,
            )
            if ok:
                responseBody = str(content)
                status = 200
                reason = "OK"
            else:
                responseBody = "Not Found"
                status = 404
                reason = "Not Found"
        case _:
            responseBody = "Method not Allowed"
            status = 405
            reason = "Method not Allowed"

    body = responseBody

    header = {
        "Server": "HTMLDrip",
        "Content-Type": "text/html",
        "Content-Length": str(len(body.encode())),
    }

    return HTTPResponse(
        status=status,
        reason=reason,
        http_version=req.http_version,
        header=header,
        body=body,
    )


def badRequest():
    header = {
        "Server": "HTMLDrip",
        "Content-Type": "text/html",
        "Content-Length": "0",
    }
    return HTTPResponse(
        status=400,
        reason="Bad Request",
        http_version="HTTP/1.1",
        header=header,
        body="",
    )
