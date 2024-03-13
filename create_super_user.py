import asyncio
import sys

from app.service_layer.users.utils import create_super_user

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Invocation error, usage: {sys.argv[0]} <email> <password>", file=sys.stderr)
        exit(1)
    asyncio.run(create_super_user(sys.argv[1], sys.argv[2]))
