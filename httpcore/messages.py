from dataclasses import dataclass


# i like to work with go and c, miss my structs and interfaces :(
# this is useful to define the data structures which will be used by the handler
@dataclass(frozen=True)
class HTTPRequest:
    method: str
    path: str
    http_version: str
    header: dict[str, str]
    body: str | None


@dataclass(frozen=True)
class HTTPResponse:
    status: int
    reason: str
    http_version: str
    header: dict[str, str]
    body: str
