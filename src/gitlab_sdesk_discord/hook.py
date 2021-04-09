from __future__ import annotations

import json
import socket
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print("This command requires exactly one argument with JSON payload.")
        return 1

    payload = json.loads(sys.argv[1])
    if False:
        return 0

    with socket.socket() as sock:
        sock.connect(("127.0.0.1", 8889))
        sock.send(json.dumps(payload).encode())

    return 0


if __name__ == "__main__":
    sys.exit(main())
