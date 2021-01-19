"""
Bot to read and generate SMU Timetable

Usage:
To Update
"""
import logging
from utility import *

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Bot

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext, CallbackQueryHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = "1563865053:AAHTgGSPVfkfdymPGrVnSy5IZ1O_lyYAbNE"

FILE, COMPUTER, MOBILE, DEVICE = range(4)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update:Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello there! Use /newTimeTable to begin!')

def error(update:Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def newTimeTable(update: Update, context: CallbackContext):
    """Ask User to select which device they using"""
    keyboard =[[
        InlineKeyboardButton("PC/Laptop", callback_data=str(COMPUTER))
    ], [
        InlineKeyboardButton('Mobile', callback_data=str(MOBILE))
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Please choose which device you are using or use /cancel to cancel the request...", reply_markup= reply_markup)

    return DEVICE

def computer(update: Update, context: CallbackContext):
    """PC/Laptop Format Ask for New Timetable"""

    query = update.callback_query

    query.answer()

    keyboard = [[InlineKeyboardButton("Direct me to Boss", url='https://boss.intranet.smu.edu.sg/TTPlanner.aspx')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(text="Download your CSV Timetable from Boss and Send it To Me or use /cancel to cancel the request.", reply_markup = reply_markup)
    
    newBot = Bot(TOKEN)

    newBot.sendPhoto(chat_id = query.message.chat.id, photo = open('./windowsBoss.png', 'rb'))

    return FILE

def mobile(update: Update, context: CallbackContext):
    """Mobile Format Ask for New Timetable"""

    query = update.callback_query

    query.answer()

    keyboard = [[InlineKeyboardButton("Direct me to Boss", url='https://boss.intranet.smu.edu.sg/TTPlanner.aspx')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(text="Download your CSV Timetable from Boss and Send it To Me or use /cancel to cancel the request.", reply_markup = reply_markup)
    newBot = Bot(TOKEN)

    newBot.sendPhoto(chat_id = query.message.chat.id, photo = open('./iosBoss.jpg', 'rb'))

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
/week - See all the lessons you have in a week
/exams - See your exams for this semester"""

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

def exams(update: Update, context: CallbackContext):
    """Call generateExams fn and return user their exams outlook"""

    USERID = str(update.message.chat.id)
    
    try:
        result = generateExams(USERID)
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
/week - See all the lessons you have in a week
/exams - See your exams for this semester"""

    update.message.reply_text(msg, parse_mode="HTML")

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))

    timeTableConv = ConversationHandler(
        entry_points=[CommandHandler('newTimeTable', newTimeTable)],
        states={
            DEVICE: [
                CallbackQueryHandler(computer, pattern='^'+str(COMPUTER)+'$'),
                CallbackQueryHandler(mobile, pattern='^'+str(MOBILE)+'$'),
                CommandHandler('cancel', cancel)
            ],
            FILE: [
                MessageHandler(Filters.document.file_extension("csv"), generate), CommandHandler('cancel', cancel), 
                MessageHandler(Filters.all, wrongType)
            ]
        },
        fallbacks = [CommandHandler('cancel', cancel)],
        allow_reentry= True
    )

    dp.add_handler(timeTableConv)
    dp.add_handler(CommandHandler('week',week))
    dp.add_handler(CommandHandler('today',seeToday))
    dp.add_handler(CommandHandler('tmr',seeTmr))
    dp.add_handler(CommandHandler('commands',seeCommands))
    dp.add_handler(CommandHandler('exams', exams))
    
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

