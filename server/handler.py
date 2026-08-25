import json
from pathlib import Path

from httpcore.messages import HTTPRequest, HTTPResponse
from storage import filestore


def handle(req: HTTPRequest, localStorage: Path) -> HTTPResponse:
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
                responseBody = ""
                status = 404
                reason = "Not Found"
        case _:
            print("Method not allowed")
            responseBody = ""
            status = 405
            reason = "Method not Allowed"

    body = responseBody

    header = {
        "Server": "HTMLDrip",
        "Content-Type": "text/plain",
        "Content-Length": str(len(body.encode())),
    }

    return HTTPResponse(
        status=status,
        reason=reason,
        http_version=req.http_version,
        header=header,
        body=body,
    )
