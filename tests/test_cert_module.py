import asyncio

from commands.crt import lookup_certificates


async def main():
    results = await lookup_certificates("example.com")

    if results is None:
        print("Erro ao consultar crt.sh")
        return

    for name in results:
        print(name)


asyncio.run(main())
