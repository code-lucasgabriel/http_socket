import signal

from server import listener

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, listener.shutdown)
    signal.signal(signal.SIGINT, listener.shutdown)
    listener.start(host="0.0.0.0", port=50051)
