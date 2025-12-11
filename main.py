import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_KEY)

SYSTEM_PROMPT = """
You are a Design Quality Assistant.
Evaluate the uploaded design according to Sber B2B style:
- Colors (brand greens, gradients)
- Shapes (rounded, soft forms)
- 3D elements consistency
- Light, toning, accents
- Typography clarity
Provide a clear, actionable improvement guide.
"""

async def analyze_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    image_bytes = await file.download_as_bytearray()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Review this design"},
                    {"type": "image", "image": image_bytes},
                ],
            },
        ],
    )

    result = response.choices[0].message.content
    await update.message.reply_text(result)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, analyze_image))
    app.run_polling()
