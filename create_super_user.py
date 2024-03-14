import asyncio
import contextlib
import sys

from app.adapters.db.session import get_async_session
from app.service_layer.users.utils import create_user

get_async_session_context = contextlib.asynccontextmanager(get_async_session)


async def create_super_user(email: str, password: str):
    async with get_async_session_context() as db:
        await create_user(db, email, password, True)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Invocation error, usage: {sys.argv[0]} <email> <password>", file=sys.stderr)
        exit(1)
    asyncio.run(create_super_user(sys.argv[1], sys.argv[2]))
