from Cogs.Tips import Trends
# for champion_counter
from bs4 import BeautifulSoup
import requests

line_one = [
'number',
'champion',
'kills',
'deaths',
'assists',
'damage',
'damage migated',
'gold earned'
]

ids = [350,154,36,34,40,102,75,62,86,98,83,518,7,54,113,26,161,516,223,61,202,31,16,117,82,90,103,79,106,37,267,112,81,85,150,48,77,115,876,101,134,45,142,43,432,114,10,887,104,240,245,35,78,888,201,497,84,15,58,13,120,33,59,17,8,711,6,266,122,498,99,51,28,121,3,56,25,32,147,2,41,875,145,1,127,23,9,235,92,420,238,38,268,110,21,105,131,18,234,254,60,53,44,69,236,221,76,126,166,24,141,164,222,64,57,20,412,89,96,27,67,111,29,50,143,429,22,4,5,119,777,523,14,91,526,163,360,68,19,421,555,12,42,133,107,55,157,517,39,246,203,11,30,80,63]

with open('trends.csv', 'w+') as f:
    line_one = ','.join(line_one)
    f.write(line_one)
    f.write("\n")
    for i in ids:
        try:
            data = list(Trends.get_trends(i).values())
            if not data:
                continue
            else:
                print(data[0])
            data = ','.join(data)
            data = f'{i},{data}'
            f.write(data)
            f.write("\n")
        except:
            continue