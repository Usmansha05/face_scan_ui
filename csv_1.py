import pandas as pd
from datetime import datetime

def mark_attendance(name):
    with open('attendance.csv', 'a') as f:
        now = datetime.now()
        dt_string = now.strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{name},{dt_string}\n')
