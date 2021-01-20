"""
Bot to read and generate SMU Timetable

Usage:
To Update
"""
import logging
from utility import *
from uuid import uuid4

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Bot, InlineQueryResultArticle, InputTextMessageContent

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext, CallbackQueryHandler, InlineQueryHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = "1563865053:AAHTgGSPVfkfdymPGrVnSy5IZ1O_lyYAbNE"

FILE, COMPUTER, MOBILE, DEVICE, ADD = range(5)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update:Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello there!\n\nThe bot is currently in v1.0. Use /newTimeTable to begin!')

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

    query.edit_message_text(text="1. Login to Boss\n2. Download your CSV Timetable from Boss\n3. Send it To Me/Drag and drop the file into chat\n\nUse /cancel to cancel the request.", reply_markup = reply_markup)
    
    newBot = Bot(TOKEN)

    newBot.sendPhoto(chat_id = query.message.chat.id, photo = open('./windowsBoss.png', 'rb'))

    return FILE

def mobile(update: Update, context: CallbackContext):
    """Mobile Format Ask for New Timetable"""

    query = update.callback_query

    query.answer()

    keyboard = [[InlineKeyboardButton("Direct me to Boss", url='https://boss.intranet.smu.edu.sg/TTPlanner.aspx')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(text="1. Login to Boss\n2. Download your CSV Timetable from Boss\n3. Follow the image and share the file to me\n\nUse /cancel to cancel the request.", reply_markup = reply_markup)
    newBot = Bot(TOKEN)

    newBot.sendPhoto(chat_id = query.message.chat.id, photo = open('./iosBoss.jpg', 'rb'))

    return FILE

def generate(update: Update, context: CallbackContext):
    """Save File into Server and Let User Know what are the available commands"""
    update.message.reply_text("Dumping your files into the File Monster...")
    USERNAME= str(update.message.chat.username)
    
    fileObj = context.bot.getFile(update.message.document.file_id)

    fileObj.download('./userFiles/'+USERNAME+'.csv')

    
    msg = """File Monster ate the File! 🙊
\n<b>Individual Commands</b>
/newTimeTable - Update your time table
/today - See your lessons for today
/tmr - See your lessons for tomorrow
/week - See all the lessons you have in a week
/exams - See your exams for this semester
/credits - For feedback & credits
\n<b>Group (Find Common Free Time)</b>
Type @smu_timetablebot in any group chat (without pressing ENTER)
Wait for the popup to appear and then select 'Add To Group'"""

    update.message.reply_text(msg, parse_mode='HTML')
    newBot = Bot(TOKEN)

    newBot.sendAnimation(chat_id = update.message.chat.id, animation = open('./group.gif','rb'))


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
    USERNAME= str(update.message.chat.username)

    try:
        result = generateToday(USERNAME)
        update.message.reply_text(result, parse_mode='HTML')
    except:
        update.message.reply_text(
            'Oops, unable to find your time table 🤐\n\nUse the command /newTimeTable to update your time table'
        )

def seeTmr(update: Update, context: CallbackContext):
    """Call generateTmr fn and return their schedule for tmr"""
    USERNAME= str(update.message.chat.username)

    try:
        result = generateTmr(USERNAME)
        update.message.reply_text(result, parse_mode='HTML')
    except:
        update.message.reply_text(
            'Oops, unable to find your time table 🤐\n\nUse the command /newTimeTable to update your time table'
        )

def week(update: Update, context: CallbackContext):
    """Call generateWeek fn and return user their week outlook"""
    USERNAME= str(update.message.chat.username)

    try:
        result = generateWeek(USERNAME)
        update.message.reply_text(result, parse_mode='HTML')
    except:
        update.message.reply_text(
            'Oops, unable to find your time table 🤐\n\nUse the command /newTimeTable to update your time table'
        )

def exams(update: Update, context: CallbackContext):
    """Call generateExams fn and return user their exams outlook"""

    USERNAME= str(update.message.chat.username)
    
    try:
        result = generateExams(USERNAME)
        update.message.reply_text(result, parse_mode='HTML')
    except:
        update.message.reply_text(
            'Oops, unable to find your time table 🤐\n\nUse the command /newTimeTable to update your time table'
        )

def seeCommands(update: Update, context: CallbackContext):
    """Generate All Commands for User to Reference"""

    msg = """<b>Individual Commands Available</b>
/newTimeTable - Update your time table
/today - See your lessons for today
/tmr - See your lessons for tomorrow
/week - See all the lessons you have in a week
/exams - See your exams for this semester
/credits - For feedback & credits
\n<b>Group (Find Common Free Time)</b>
Type @smu_timetablebot in any group chat (without pressing ENTER)
Wait for the popup to appear and then select 'Add To Group'"""

    update.message.reply_text(msg, parse_mode="HTML")

def commonTime(update: Update, context: CallbackContext):
    """Handle Inline Query"""
    # print('update=',update)
    keyboard = [
        [InlineKeyboardButton('Get Common Time', callback_data= str(ADD))],
        [InlineKeyboardButton('Upload Timetable to File Monster', url = 'https://telegram.me/smu_timetablebot')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    results = [
        InlineQueryResultArticle(
            id= uuid4(),
            title='Add to Chat',
            input_message_content=InputTextMessageContent('Select Get Common Time to find the common free time that works for anyone in the group.\n\nIf you have not fed File Monster (@smu_timetablebot) your timetable click Upload Timetable and follow the instructions there!'),
            reply_markup = reply_markup
        )
    ]

    update.inline_query.answer(results)

def groupAdd(update: Update, context: CallbackContext):
    """Compile Timetables and return free timeslots"""

    query = update.callback_query

    query.answer()
    # print('query=',query)
    USERNAME = query.from_user.username
    chatInstance = query.chat_instance
    commonSchedule = getCommon(chatInstance, USERNAME)

    if commonSchedule == 'noTimeTable':
        newBot = Bot(TOKEN)
        newBot.sendMessage(chat_id=query.from_user.id, text ="Oh no! File Monster doesn't have your timetable.\n\nUse /newTimeTable to feed File Monster your timetable before adding your timetable in the chat group.")
    elif commonSchedule == 'timeTableOutdated':
        newBot = Bot(TOKEN)
        newBot.sendMessage(chat_id=query.from_user.id, text ="Oh no! Your timetable is outdated!\n\nUse /newTimeTable to feed File Monster your timetable before adding your timetable in the chat group.")
    else:
        keyboard = [
            [InlineKeyboardButton('Add/Update/Refresh', callback_data= str(ADD))],
            [InlineKeyboardButton('Upload Timetable to File Monster', url = 'https://telegram.me/smu_timetablebot')]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        output='<u>Common Free Time</u>\n\n'
        days = ['Mon','Tue','Wed','Thu','Fri']
        for key in commonSchedule:
            if key in days:
                output+='<b>'+key+'</b>'

                for el in commonSchedule[key]:
                    output += '\n'+convertTime(el[0]) +' - '+convertTime(el[1])

                output+='\n\n'

        output+= "<b>Users' Timetable Added:</b>"

        for el in commonSchedule['addedUsers']:
            output+= '\n'+el

        output+= '\n\n<b>Note</b>\n<i>Feed File Monster your Timetable before adding your Timetable here'

        output+= '\n\nSchedule Accurate from\n'+commonSchedule['startDate']+' to '+commonSchedule['endDate']+'</i>'
        
        query.edit_message_text(text=output, reply_markup = reply_markup, parse_mode='HTML')

def showCredits(update: Update, context: CallbackContext):
    """Show credits to user"""
    update.message.reply_text(
        "This bot is created as a side project drawing inspirations from @SMUTimetableBot.\n\nThe original bot is no longer working and I've decided to create my own.\n\nFor and issues or feedback HMU at @YiHao123 or connect with me on LinkedIn at https://www.linkedin.com/in/yi-hao-lee-403395203/"
    )

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    #New Filter Class for Groups & Private
    # privateChatFilter = Filters.chat_type.private

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
    dp.add_handler(InlineQueryHandler(commonTime))
    dp.add_handler(CallbackQueryHandler(groupAdd, pattern='^'+str(ADD)+'$'))
    dp.add_handler(CommandHandler('credits', showCredits))

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

