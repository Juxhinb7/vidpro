import asyncio

PROGRESS: dict[str, int] = {}
lock = asyncio.Lock()