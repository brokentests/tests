'''Какой вывод в консоль?'''

import asyncio

async def foo():
    print("start")
    await asyncio.sleep(1)
    print("end")

async def main0():
    task1 = foo()
    task2 = foo()
    await task1
    await task2

async def main1():
    task1 = asyncio.create_task(foo())
    task2 = asyncio.create_task(foo())
    await task1
    await task2

asyncio.run(main0())
print('-')
asyncio.run(main1())