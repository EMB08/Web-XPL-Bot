import asyncio

import aiohttp


async def main():
    url = "https://crt.sh/?q=example.com&output=json"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    names = set()

    for certificate in data:
        certificate_names = certificate.get("name_value", "")

        for name in certificate_names.splitlines():
            names.add(name)

    domain = "example.com"

    for name in sorted(names):
        if "@" in name:
             continue

        if " " in name:
            continue

        if name == domain or name.endswith("." + domain):
            print(name)



asyncio.run(main())
