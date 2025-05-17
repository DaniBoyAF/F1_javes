import discord
import asyncio

async def send_pdf_to_discord(filepath, channel_id,bot_token):
    intents =discord.Intents.default()
    client = discord.Client(intents=intents)
    @client.event
    async def on_ready():
        channel=client.get_channel(channel_id)
        if channel:
            with open(filepath,"rb") as f:
                await channel.send("Relatório F1:", file=discord.File(f, filename="relatorio_f1.pdf"))
            await client.close()

    await client.start(bot_token)