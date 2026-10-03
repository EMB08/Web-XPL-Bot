import asyncio

from commands.gau import lookup_gau


async def main():
    results = await lookup_gau("example.com")

    if results is None:
        print("Erro ao executar o GAU.")
        return

    print(f"Encontradas {len(results)} URLs.")

    for url in results[:20]:
        print(url)


asyncio.run(main())
