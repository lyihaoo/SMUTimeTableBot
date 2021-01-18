import pandas as pd
import random
from dateutil.parser import *
from datetime import datetime

emojiArr = ['🤯','😎','🥳','🤩','🤤']
dayArr = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']

def getDF(USERID):
    """Read and Return Dataframe Object"""
    df = pd.read_csv('./userFiles/'+USERID+'.csv')
    return df

def generateToday(USERID):
    """Generate list of lessons for today"""
    df = getDF(USERID)

    filterClass = df[df['Meeting Type'] == 'CLASS'].sort_values(by='Start Time')
    if parse(filterClass['End Date'][0]) < datetime.now():
        return 'Oops, your timetable is out dated 🤐\n\nUse the command /newTimeTable to update your time table'

    dayToday = datetime.today().weekday()

    if dayToday >= 5:
        return 'Its the Weekends! 🎉 Go have fun 🎈'
    else:
        filterDay = filterClass[filterClass['Day(s)'] == dayArr[dayToday]]
        temp = ''
        toReturn = 'Today is <b>'+dayArr[dayToday]+'</b> you have:\n'

        for index, row in filterDay.iterrows():
            temp += '<b>'+ convertTime(row['Start Time']) + ' - ' + convertTime(row['End Time']) + ' (' + row['Venue'] + ')</b> | '+ row['Sect'] +' | <b>' + row['Code'] + '</b> <i>' + row['Description'] +'</i>\n\n'

        if temp == '':
            toReturn += 'Nothing! Make full use of your free time! '+random.choice(emojiArr)
        else:
            toReturn += temp
        
        return toReturn

def generateTmr(USERID):
    """Generate list of lessons for Tmr"""
    df = getDF(USERID)

    filterClass = df[df['Meeting Type'] == 'CLASS'].sort_values(by='Start Time')
    if parse(filterClass['End Date'][0]) < datetime.now():
        return 'Oops, your timetable is out dated 🤐\n\nUse the command /newTimeTable to update your time table'

    dayToday = datetime.today().weekday()

    if dayToday == 6:
        dayTmr = 0
    else:
        dayTmr = dayToday + 1

    if dayTmr >= 5:
        return 'Its the Weekends tomorrow! 🎉 Rest well 🎈'
    else:
        filterDay = filterClass[filterClass['Day(s)'] == dayArr[dayTmr]]
        temp = ''
        toReturn = 'Tomorrow is <b>'+dayArr[dayTmr]+'</b> you have:\n'

        for index, row in filterDay.iterrows():
            temp += '<b>'+ convertTime(row['Start Time']) + ' - ' + convertTime(row['End Time']) + ' (' + row['Venue'] + ')</b> | '+ row['Sect'] +' | <b>' + row['Code'] + '</b> <i>' + row['Description'] +'</i>\n\n'

        if temp == '':
            toReturn += 'Nothing! Make full use of your free time! '+random.choice(emojiArr)
        else:
            toReturn += temp
        
        return toReturn

def generateWeek(USERID):
    """Generate an array of Day Objects to be sent back to the User"""
    df = getDF(USERID)

    extracted = df[df['Meeting Type'] == 'CLASS'].sort_values(by='Start Time')

    if parse(extracted['End Date'][0]) < datetime.now():
        return 'Oops, your timetable is out dated 🤐\n\nUse the command /newTimeTable to update your time table'

    resultArr = {'Mon':[], 'Tue':[], 'Wed':[], 'Thu':[], 'Fri':[]}

    for index, row in extracted.iterrows():
        temp = '<b>'+ convertTime(row['Start Time']) + ' - ' + convertTime(row['End Time']) + ' (' + row['Venue'] + ')</b> | '+ row['Sect'] +' | <b>' + row['Code'] + '</b> <i>' + row['Description'] +'</i>'

        resultArr[row['Day(s)']].append(temp)
    
    toReturn = ''

    for key in resultArr:
        
        toReturn += '<b>'+key+'</b>\n'

        if resultArr[key] != []:
            for element in resultArr[key]:
                toReturn += element +'\n\n'
        else:
            toReturn += 'Free Day! '+random.choice(emojiArr)+'\n\n'
    
    return toReturn

def generateExams(USERID):
    df = getDF(USERID)

    extracted = df[df['Meeting Type'] == 'EXAM']

    extracted2 = extracted.assign(dateObj = pd.to_datetime(extracted['Start Date'], infer_datetime_format=True))
    
    sortedDF = extracted2.sort_values(['dateObj', 'Start Time'])

    if sortedDF['dateObj'].iloc[-1] < datetime.now():
        return 'Oops, your timetable is out dated 🤐\n\nUse the command /newTimeTable to update your time table'

    toReturn = ''

    for index, row in sortedDF.iterrows():
        toReturn += '<b>'+ row['Start Date'] +'</b> | '+ convertTime(row['Start Time']) + ' - ' + convertTime(row['End Time']) + ' | <b>' + row['Code'] + '</b> <i>' + row['Description'] +'</i>\n'

    if toReturn == '':
        return 'Woohoo! You have no exams for this semester! '+random.choice(emojiArr)
    else:
        return toReturn

def convertTime(x):
    """Utility Function to Convert 24 Hour input to 12 Hour Input"""
    x = x.split(':')

    if int(x[0]) > 12:
        return str(int(x[0])-12) + ':' + x[1] + ' PM'
    elif int(x[0]) == 12:
        return ':'.join(x) + ' PM'
    else:
        return ':'.join(x) + ' AM'

# print(generateToday('test'))
# print(generateTmr('test'))
# print(generateWeek('test'))
# print(generateExams('test'))