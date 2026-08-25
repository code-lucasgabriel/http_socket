from pathlib import Path


def find(storage: Path, name: str) -> tuple[str | None, bool]:
    print(f"finding file: {name}")
    filePath = storage / name

    if filePath.parent != storage:
        return (
            "doing some path traversal on my file system eeeh kid? nice one, but i was prepared for this!",
            True,
        )

    # verify if file actually exists
    if filePath.is_file():
        return filePath.read_text("utf_8"), True

    print(f"file not found: {name}")
    return None, False
