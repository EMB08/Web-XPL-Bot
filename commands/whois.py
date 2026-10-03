import asyncio
import re

WHOIS_PATH = "/usr/bin/whois"


def parse_whois(output: str):
    data = {}

    field_mapping = {
        "domain": "Domain Name",
        "owner": "Registrant",
        "created": "Creation Date",
        "changed": "Updated Date",
        "expires": "Registry Expiry Date",
        "nserver": "Name Server",
    }

    whois_fields = {
        "Domain Name",
        "Registrar",
        "Registrant",
        "Creation Date",
        "Updated Date",
        "Registry Expiry Date",
        "Name Server",
        "DNSSEC",
    }

    for line in output.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
        elif ":" not in line and re.match(r"^\s*\w+\s+", line):
            parts = line.split(None, 1)

            if len(parts) != 2:
                continue

            key, value = parts
        else:
            continue

        key = key.strip()
        value = value.strip()

        key = field_mapping.get(key.lower(), key)

        if key not in whois_fields or not value:
            continue

        if key == "Name Server":
            data.setdefault(key, [])
            data[key].append(value)
        else:
            data[key] = value

    return data

async def lookup_whois(domain: str):
    process = await asyncio.create_subprocess_exec(
        WHOIS_PATH,
        domain,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        return None

    result = stdout.decode()

    return parse_whois(result)
