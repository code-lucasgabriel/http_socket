from pathlib import Path

from logger.logger import getLogger

log = getLogger(__name__)


def find(localStorage: Path, name: str) -> tuple[str | None, bool]:
    # this is the package who does the job of finding the file in the public localStorage
    # notice it does not let one do path traversal on the server machine, as this is
    # very dangerous
    log.info(f"finding requested file: {name}")
    filePath = localStorage / name

    if not (localStorage / name).resolve().is_relative_to(localStorage.resolve()):
        return (
            "doing some path traversal on my file system eeeh kid? nice one, but i was prepared for this!",
            False,
        )

    # verify if file actually exists
    if filePath.is_file():
        return filePath.read_text("utf_8"), True

    log.warning(f"file not found: {name}")
    return None, False
