import asyncio
import os


async def say(msg: str):
    if msg:
        msg = msg.replace('"', '').replace('\\b', '')

        def worker():
            os.system('afplay /System/Library/Sounds/Sosumi.aiff')
            os.system(f'say "{msg}"')

        async def a_worker():
            await asyncio.get_event_loop().run_in_executor(None, worker)

        asyncio.create_task(a_worker())
