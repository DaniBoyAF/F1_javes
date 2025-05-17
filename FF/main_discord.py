from FF.export_pdf import export_all_data_to_pdf
from FF.discord import send_pdf_to_discord
import asyncio

# Gere o PDF
export_all_data_to_pdf('relatorio_f1.pdf')

# Envie para o Discord
channel_id = 123456789012345678  # Substitua pelo ID do seu canal
bot_token = "SEU_TOKEN_DO_BOT"   # Substitua pelo token do seu bot

asyncio.run(send_pdf_to_discord('relatorio_f1.pdf', channel_id, bot_token))