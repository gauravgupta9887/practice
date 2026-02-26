import asyncio


async def main():
    await asyncio.sleep(4)
    await asyncio.sleep(2)
    return "Hello"

print(asyncio.run(main()))
