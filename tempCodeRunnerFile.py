import pandas as pd
import random
from dateutil.parser import *
from datetime import datetime, timedelta
import json
import time

emojiArr = ['🤯','😎','🥳','🤩','🤤']
dayArr = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
GMT = timedelta(hours=8)

print((datetime.today()+GMT).weekday())