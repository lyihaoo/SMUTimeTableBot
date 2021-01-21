import pandas as pd
import random
from dateutil.parser import *
from datetime import datetime
import json
import time

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
        return 'Oops, your timetable is out dated 🤐\n\nUse the command /newTimeTable to feed File Monster your new time table'

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
        return 'Oops, your timetable is out dated 🤐\n\nUse the command /newTimeTable to feed File Monster your new time table'

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
        return 'Oops, your timetable is out dated 🤐\n\nUse the command /newTimeTable to feed File Monster your new time table'

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
        return 'Oops, your timetable is out dated 🤐\n\nUse the command /newTimeTable to feed File Monster your new time table'

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

def getStrpTime(x):
    return time.strptime(x, '%H:%M')

def getCommon(chatInstance, USERNAME):
    #try to load previous data if error = no previous data, create new data file
    try:
        with open('./commonTimeFolder/'+chatInstance+'.json','r') as inFile:
            data = json.load(inFile)
        
        if parse(data['endDate']) < datetime.now():
            data = {
            'addedUsers':[],
            'Mon':[['8:15','23:59']],
            'Tue':[['8:15','23:59']],
            'Wed':[['8:15','23:59']],
            'Thu':[['8:15','23:59']],
            'Fri':[['8:15','23:59']],
            'startDate': '',
            'endDate': ''
        }
    except:
        data = {
            'addedUsers':[],
            'Mon':[['8:15','23:59']],
            'Tue':[['8:15','23:59']],
            'Wed':[['8:15','23:59']],
            'Thu':[['8:15','23:59']],
            'Fri':[['8:15','23:59']],
            'startDate': '',
            'endDate': ''
        }
    
    #Check if user's timetable has already been added, if so return None
    if USERNAME in data['addedUsers']:
        return data
    
    #try to load user's time table, if error = user has not uploaded their timetable, return noTimeTable
    try:
        df = getDF(USERNAME)
    except:
        return 'noTimeTable'
    
    #Filter Class & sort values according to day and start time
    extractedClass = df[df['Meeting Type'] == 'CLASS'].sort_values(['Day(s)','Start Time'])

    #If time table outdated return timeTableOutdated
    if parse(extractedClass['End Date'][0]) < datetime.now():
        return 'timeTableOutdated'

    if data['startDate'] == '':
        data['startDate'] = extractedClass['Start Date'][0]
        data['endDate'] = extractedClass['End Date'][0]

    bufferTimeConvert = {'11:30':'12:00','15:15':'15:30','18:45':'19:00'}

    #iterate through each row of the dataframe
    for index, row in extractedClass.iterrows():

        dayToModify = row['Day(s)']
        dataToModify = data[dayToModify] #this is an array of free time
        startTimeOfLesson = getStrpTime(row['Start Time'])
        endTimeOfLesson = getStrpTime(bufferTimeConvert[row['End Time']])

        temp = []
        count = 0
        
        for element in dataToModify:
            #check if start time is in between the start and end time of the element
            if startTimeOfLesson > getStrpTime(element[0]) and startTimeOfLesson< getStrpTime(element[1]):
                # if startTimeOfLesson > getStrpTime(element[0]):
                temp.append([element[0], row['Start Time']])

            #check if end time is in between the start and end time of the element
            if endTimeOfLesson >= getStrpTime(element[0]) and endTimeOfLesson <= getStrpTime(element[1]):
                if endTimeOfLesson == getStrpTime(element[0]):
                    temp+= dataToModify[count:]
                    break
                elif endTimeOfLesson == getStrpTime(element[1]):
                    temp+= dataToModify[count+1:]
                    break
                else:
                    temp.append([bufferTimeConvert[row['End Time']], element[1]])
                    temp+= dataToModify[count+1:]
                    break
            count+=1
        if temp != []:
            data[dayToModify] = temp
    
    data['addedUsers'].append(USERNAME)

    #save data to json file
    with open('./commonTimeFolder/'+chatInstance+'.json','w') as outfile:
        json.dump(data, outfile, indent=4)

    return data

