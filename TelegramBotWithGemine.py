import telebot
import requests
import json
import re

#  Your telegram api key
TELEGRAM_TOKEN = '#####################'

# Your Gemini api key (from Google AI Studio)
GEMINI_API_KEY = '#####################'

# URL For model
GEMINI_API_URL = '###################'

bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "👋 Привет! Я бот на базе *Google Gemini 2.0 Flash*.\n"
        "Задай мне вопрос, и я постараюсь ответить красиво и понятно 💬",
        parse_mode='Markdown'
    )


# 🔸 Основной обработчик сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_query = message.text.strip()

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    data = {
        "contents": [
            {"parts": [{"text": user_query}]}
        ]
    }

    try:
        # 🔹 Отправляем запрос к Gemini
        response = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()

        response_json = response.json()
        ai_response = response_json["candidates"][0]["content"]["parts"][0]["text"].strip()

        # 🔹 Обрезаем слишком длинный ответ
        max_length = 3500
        response_text = f"💡 *Ответ от Gemini:*\n\n{ai_response}"

        # 🔹 Авто-форматирование кода (если есть ключевые слова)
        code_keywords = ["def ", "class ", "import ", "print(", "{", "}", ";", "#include", "public ", "private "]
        if any(k in ai_response for k in code_keywords) and "```" not in ai_response:
            ai_response = f"```python\n{ai_response}\n```"

        # 🔹 Очистка Markdown-символов, чтобы Telegram не ломал форматирование
        ai_response = re.sub(r'[_*`]', r'', ai_response)

        # 🔹 Финальное сообщение с красивым стилем
        text = f"💡 *Ответ от Gemini:*\n\n{ai_response}"

        for i in range(0, len(response_text), max_length):
            part = response_text[i:i + max_length]
            bot.send_message(message.chat.id, part, parse_mode='Markdown')

    except Exception as e:
        bot.reply_to(
            message,
            f"⚠️ Ошибка: {str(e)}\nПроверь API-ключ или формат запроса."
        )


# 🔹 Запуск бота (постоянный опрос)
bot.polling(none_stop=True)