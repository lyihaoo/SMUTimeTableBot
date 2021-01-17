"""
Bot to read and generate SMU Timetable

Usage:
To Update
"""
import logging
from utility import *

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

FILE = range(1)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update:Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update:Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def error(update:Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def newTimeTable(update: Update, context: CallbackContext):
    """Ask for New Timetable"""
    update.message.reply_text("Send CSV Timetable")

    return FILE

def generate(update: Update, context: CallbackContext):
    """Save File into Server and Let User Know what are the available commands"""
    update.message.reply_text("Generating Assets")
    userID = str(update.message.chat.id)
    
    fileObj = context.bot.getFile(update.message.document.file_id)

    fileObj.download('./userFiles/'+userID+'.csv')

def cancel(update: Update, context: CallbackContext):
    """Handle Cancel Requests"""
    update.message.reply_text('Request Cancelled')

    return ConversationHandler.END

def week(update: Update, context: CallbackContext):
    """Call generateWeek fn and return user their week outlook"""
    USERID = str(update.message.chat.id)

    result = generateWeek(USERID)
    update.message.reply_text(result, parse_mode='HTML')


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1563865053:AAHTgGSPVfkfdymPGrVnSy5IZ1O_lyYAbNE", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('newTimeTable', newTimeTable)],
        states={
            FILE: [MessageHandler(Filters.document.file_extension("csv"), generate)]
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('week',week))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

