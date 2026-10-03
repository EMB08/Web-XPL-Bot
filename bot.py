import os
import ipaddress

import discord
from discord import app_commands
from dotenv import load_dotenv

from commands.ipinfo import lookup_ip
from commands.gau import lookup_gau, is_valid_domain
from commands.nmap import lookup_nmap
from commands.whois import lookup_whois

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))


class WebXPLBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        guild = discord.Object(id=GUILD_ID)

        self.tree.copy_global_to(guild=guild)

        synced = await self.tree.sync(guild=guild)

        print("Comandos sincronizados:")

        for command in synced:
            print(f"- /{command.name}")


bot = WebXPLBot()


@bot.tree.command(name="ping", description="Verifica se o bot está funcionando.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong! 🏓")


@bot.tree.command(name="ipinfo", description="Consulta informações sobre um endereço IP.")
@app_commands.describe(ip="Endereço IP que será consultado.")
async def ipinfo(interaction: discord.Interaction, ip: str):

    try:
        ipaddress.ip_address(ip)

    except ValueError:
        await interaction.response.send_message(
            "❌ O valor informado não é um endereço IP válido."
    )
        return

    data = await lookup_ip(ip)

    if data is None:
        await interaction.response.send_message(
            "Não foi possível consultar esse IP."
        )
        return

    await interaction.response.send_message(
        f"IP: {data.get('ip', 'Não informado')}\n"
        f"Hostname: {data.get('hostname', 'Não informado')}\n"
        f"Organização: {data.get('org', 'Não informado')}\n"
        f"Localização: {data.get('city', 'Não informado')}, "
        f"{data.get('region', 'Não informado')}, "
        f"{data.get('country', 'Não informado')}\n"
        f"Timezone: {data.get('timezone', 'Não informado')}"
    )

@bot.tree.command(name="gau", description="Coleta URLs públicas de um domínio.")
@app_commands.describe(domain="Domínio que será consultado.")
async def gau(interaction: discord.Interaction, domain: str):
    await interaction.response.defer()

    if not is_valid_domain(domain):
        await interaction.followup.send(
            "❌ O domínio informado é inválido."
        )
        return

    results = await lookup_gau(domain)

    if results is None:
        await interaction.followup.send(
            "❌ Não foi possível executar a consulta GAU."
        )
        return

    if not results:
        await interaction.followup.send(
            "ℹ️ Nenhuma URL encontrada."
        )
        return

    output = "\n".join(results[:20])

    await interaction.followup.send(
        f"🔎 **GAU — {domain}**\n"
        f"Encontradas: {len(results)} URLs\n\n"
        f"```text\n{output}\n```"
    )

@bot.tree.command(name="nmap", description="Realiza uma varredura básica com Nmap.")
@app_commands.describe(host="Host que será consultado.")
async def nmap(interaction: discord.Interaction, host: str):
    await interaction.response.defer()

    result = await lookup_nmap(host)

    if result is None:
        await interaction.followup.send(
            "❌ Não foi possível executar a consulta Nmap."
        )
        return

    if not result:
        await interaction.followup.send(
            "❌ O host informado não foi encontrado ou não pôde ser resolvido."
        )
        return

    await interaction.followup.send(
        f"🔎 **Nmap — {host}**\n"
        f"```text\n{result}\n```"
    )

@bot.tree.command(name="whois", description="Consulta informações de registro de um domínio.")
@app_commands.describe(domain="Domínio que será consultado.")
async def whois(interaction: discord.Interaction, domain: str):
    await interaction.response.defer()

    data = await lookup_whois(domain)

    if data is None:
        await interaction.followup.send(
            "❌ Não foi possível executar a consulta WHOIS."
        )
        return

    name_servers = data.get("Name Server", [])

    if name_servers:
        formatted_name_servers = "\n".join(
            f"- {server}" for server in name_servers
        )
    else:
        formatted_name_servers = "Não informado"

    await interaction.followup.send(
        f"🔎 **WHOIS — {domain}**\n\n"
        f"**Domínio:** {data.get('Domain Name', 'Não informado')}\n"
        f"**Registrar:** {data.get('Registrar', 'Não informado')}\n"
        f"**Criado em:** {data.get('Creation Date', 'Não informado')}\n"
        f"**Atualizado em:** {data.get('Updated Date', 'Não informado')}\n"
        f"**Expira em:** {data.get('Registry Expiry Date', 'Não informado')}\n"
        f"**DNSSEC:** {data.get('DNSSEC', 'Não informado')}\n\n"
        f"**Name Servers:**\n{formatted_name_servers}"
    )

bot.run(TOKEN)
