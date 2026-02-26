import asyncio
import time


async def func1():
    for i in range(5):
        print("Inside func 1")
        await asyncio.sleep(1)


async def func2():
    for i in range(5):
        print("Inside func 2")
        await asyncio.sleep(0.8)


start = time.time()
async_tasks = asyncio.gather(func1(), func2())
asyncio.get_event_loop().run_until_complete(async_tasks)
end = time.time()
print("Asyncio took {(round(end-start), 2)} seconds")
