import aiohttp


async def lookup_certificates(domain: str):
    url = f"https://crt.sh/?q={domain}&output=json"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:

            if response.status != 200:
                return None

            data = await response.json()

    names = set()

    for certificate in data:
        certificate_names = certificate.get("name_value", "")

        for name in certificate_names.splitlines():
            names.add(name)

    results = []

    for name in sorted(names):
        if "@" in name:
            continue

        if " " in name:
            continue

        if name == domain or name.endswith("." + domain):
            results.append(name)

    return results
