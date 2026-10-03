import asyncio

from commands.whois import lookup_whois


async def main():
    result = await lookup_whois("example.com")

    if result is None:
        print("Erro ao executar o WHOIS.")
        return

    print(result)


asyncio.run(main())
