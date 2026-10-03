import asyncio

NMAP_PATH = "/usr/bin/nmap"


async def lookup_nmap(host: str):
    process = await asyncio.create_subprocess_exec(
        NMAP_PATH,
        host,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    try:
        stdout, stderr = await asyncio.wait_for(
            process.communicate(),
            timeout=30
        )

    except asyncio.TimeoutError:
        process.kill()
        await process.wait()
        return None

    result = stdout.decode()

    if process.returncode != 0:
        return None

    if "Nmap done: 0 IP addresses" in result:
        return []

    return result
