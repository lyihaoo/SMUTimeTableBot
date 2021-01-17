import pandas as pd

def generateWeek(USERID):
    """Generate an array of Day Objects to be sent back to the User"""
    df = pd.read_csv('./userFiles/'+USERID+'.csv')

    extracted = df[df['Meeting Type'] == 'CLASS'].sort_values(by='Start Time')

    resultArr = {'Mon':[], 'Tue':[], 'Wed':[], 'Thu':[], 'Fri':[]}

    for index, row in extracted.iterrows():
            temp = '<b>'+ convertTime(row['Start Time']) + ' - ' + convertTime(row['End Time']) + ' (' + row['Venue'] + ')</b> | '+ row['Sect'] +' | <b>' + row['Code'] + '</b> <i>' + row['Description'] +'</i>'

            resultArr[row['Day(s)']].append(temp)
    
    toReturn = ''

    for key in resultArr:
        
        # if key == 'Mon':
        #     toReturn += '<b>Mon</b>\n'
        # else:
        #     toReturn += '\n<b>'+ key +'</b>\n'
        
        toReturn += '<b>'+key+'</b>\n'


        if resultArr[key] != []:
            for element in resultArr[key]:
                toReturn += element +'\n\n'
        else:
            toReturn += 'Free Day!\n\n'
    
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

