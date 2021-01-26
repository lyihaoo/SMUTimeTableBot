def convertTime(x):
    """Utility Function to Convert 24 Hour input to 12 Hour Input"""
    x = x.split(':')

    if int(x[0]) > 12:
        return str(int(x[0])-12) + ':' + x[1] + ' PM'
    elif int(x[0]) == 12:
        return ':'.join(x) + ' PM'
    else:
        return ':'.join(x) + ' AM'

print(convertTime('17:00'))