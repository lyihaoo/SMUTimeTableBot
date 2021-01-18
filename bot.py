"""
Bot to read and generate SMU Timetable

Usage:
To Update
"""
import logging
from utility import *

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup
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
    update.message.reply_text('Hello there! Use /newTimeTable to begin!')

def error(update:Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def newTimeTable(update: Update, context: CallbackContext):
    """Ask for New Timetable"""
    keyboard = [[InlineKeyboardButton("Direct me to Boss", url='https://boss.intranet.smu.edu.sg/TTPlanner.aspx')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Download your CSV Timetable from Boss and Send it To Me or use /cancel to cancel the request.", reply_markup = reply_markup)

    return FILE

def generate(update: Update, context: CallbackContext):
    """Save File into Server and Let User Know what are the available commands"""
    update.message.reply_text("Dumping your files into the File Monster...")
    userID = str(update.message.chat.id)
    
    fileObj = context.bot.getFile(update.message.document.file_id)

    fileObj.download('./userFiles/'+userID+'.csv')

    
    msg = """File Monster ate the File! 🙊
\n<b>Commands</b>
/newTimeTable - Update your time table
/today - See your lessons for today
/tmr - See your lessons for tomorrow
/week - See all the lessons you have in a week"""

    update.message.reply_text(msg, parse_mode='HTML')

    return ConversationHandler.END

def wrongType(update: Update, context: CallbackContext):
    """Let User Know Error"""
    
    msg = """Oops! Please only send me a valid .CSV file downloaded from BOSS.
\nIf you would like to retry just upload or drag and drop another file.
If you would like to cancel type /cancel."""

    update.message.reply_text(msg)
    return FILE

def cancel(update: Update, context: CallbackContext):
    """Handle Cancel Requests"""
    update.message.reply_text('Request Cancelled')

    return ConversationHandler.END

def seeToday(update: Update, context: CallbackContext):
    """Call generateToday fn and return user their lesson for today"""
    USERID = str(update.message.chat.id)

    try:
        result = generateToday(USERID)
        update.message.reply_text(result, parse_mode='HTML')
    except:
        update.message.reply_text(
            'Oops, unable to find your time table 🤐\n\nUse the command /newTimeTable to update your time table'
        )

def seeTmr(update: Update, context: CallbackContext):
    """Call generateTmr fn and return their schedule for tmr"""
    USERID = str(update.message.chat.id)

    try:
        result = generateTmr(USERID)
        update.message.reply_text(result, parse_mode='HTML')
    except:
        update.message.reply_text(
            'Oops, unable to find your time table 🤐\n\nUse the command /newTimeTable to update your time table'
        )

def week(update: Update, context: CallbackContext):
    """Call generateWeek fn and return user their week outlook"""
    USERID = str(update.message.chat.id)

    try:
        result = generateWeek(USERID)
        update.message.reply_text(result, parse_mode='HTML')
    except:
        update.message.reply_text(
            'Oops, unable to find your time table 🤐\n\nUse the command /newTimeTable to update your time table'
        )

def seeCommands(update: Update, context: CallbackContext):
    """Generate All Commands for User to Reference"""

    msg = """<b>Commands Available</b>
/newTimeTable - Update your time table
/today - See your lessons for today
/tmr - See your lessons for tomorrow
/week - See all the lessons you have in a week"""

    update.message.reply_text(msg, parse_mode="HTML")

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

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('newTimeTable', newTimeTable)],
        states={
            FILE: [MessageHandler(Filters.document.file_extension("csv"), generate), CommandHandler('cancel', cancel), MessageHandler(Filters.all, wrongType)]
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('week',week))
    dp.add_handler(CommandHandler('today',seeToday))
    dp.add_handler(CommandHandler('tmr',seeTmr))
    dp.add_handler(CommandHandler('commands',seeCommands))
    
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

