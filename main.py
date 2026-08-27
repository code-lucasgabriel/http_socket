import signal

from server import listener

if __name__ == "__main__":
    # this is the entrypoint of the server
    signal.signal(signal.SIGTERM, listener.shutdown)  # graceful shutdown
    signal.signal(signal.SIGINT, listener.shutdown)  # graceful shutdown
    listener.start(host="0.0.0.0", port=50051)
