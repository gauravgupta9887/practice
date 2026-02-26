import asyncio


async def main():
    print("Hello")
    return "HI"

print(asyncio.run(main()))
