import ipaddress
import aiohttp


async def lookup_ip(ip: str):
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return None

    url = f"https://ipinfo.io/{ip}/json"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            
            if response.status != 200:
                return None

            data = await response.json()

    return data
