import logging
from find_product_dialog import ( find_product_close,
                                 find_product_dontknow, find_product_filters,
                                 find_product_request, find_product_start)
from handlers import answer_text, greet_user, help_message, last_request, clear_data
import settings_bot
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)

logging.basicConfig(filename="bot.log", level=logging.INFO)

def main():
    mybot = Updater(settings_bot.API_KEY, use_context=True)

    dp = mybot.dispatcher

    find_product = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Поиск продукта на OZON)$'), find_product_start)
        ],
        states={
            "request": [MessageHandler(Filters.text, find_product_request)],
            "filters": [MessageHandler(Filters.regex('^(По цене|По цене и рейтингу|По рейтингу и кол-ву отзывов)$'), find_product_filters)],
            "close": [MessageHandler(Filters.regex('^(Далее)$'), find_product_close)]
        },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location, find_product_dontknow)
        ]
    )

    dp.add_handler(find_product)
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("help", help_message))
    dp.add_handler(MessageHandler(Filters.regex('^(Справка)$'), help_message))
    dp.add_handler(MessageHandler(Filters.regex('^(Показать последний результат)$'), last_request))
    dp.add_handler(MessageHandler(Filters.regex('^(Очистить данные по товарам)$'), clear_data))
    dp.add_handler(MessageHandler(Filters.text, answer_text))

    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()
