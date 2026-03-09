import requests
import os
from dotenv import load_dotenv
from ...domain.services.notifications import INotificatorService

load_dotenv()

class TelegramNotificator(INotificatorService):

    def send(self, mensaje: str) -> None:

        """ 
        Envía una alerta por Telegram
        """

        token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        
        payload = {
            "chat_id": chat_id,
            "text": mensaje,
            "parse_mode": "Markdown"
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
        except Exception as e:
            print(f"❌ Error enviando Telegram: {e}")
