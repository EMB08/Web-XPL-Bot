import asyncio
import re
import shutil
import os

GAU_PATH = shutil.which("gau")

if GAU_PATH is None: GAU_PATH = os.path.expanduser("~/go/bin/gau")

def is_valid_domain(domain: str):
    pattern = r"^(?=.{1,253}$)(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}$"

    return re.fullmatch(pattern, domain) is not None


async def lookup_gau(domain: str):
    if GAU_PATH is None: 
        return None

    try:
        process = await asyncio.create_subprocess_exec(
            GAU_PATH,
            "--timeout",
            "10",
            "--providers",
            "urlscan",
            domain,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await asyncio.wait_for(
            process.communicate(),
            timeout=30
        )

    except asyncio.TimeoutError:
        process.kill()
        await process.wait()
        return None

    if process.returncode != 0:
        return None

    urls = stdout.decode().splitlines()

    urls = sorted(set(urls))

    return urls
