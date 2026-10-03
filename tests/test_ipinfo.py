import asyncio

from commands.ipinfo import lookup_ip


async def main():
    data = await lookup_ip("8.8.8.8")
    print(data)


asyncio.run(main())
