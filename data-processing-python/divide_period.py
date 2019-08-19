import csv
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from test import read_data
from datetime import *

"""
Divide dataset into different periods and save into files
"""

parliament_terms = [
    {
        "number": 1,
        "begin": "Sep. 24, 1867",
        "end": "Jul. 8, 1872",
        "party": ["Conservative"]
    },
    {
        "number": 2,
        "begin": "Sep. 3, 1872",
        "end": "Jan. 2, 1874",
        "party": ["Conservative","Liberal"]
    },
    {
        "number": 3,
        "begin": "Feb. 21, 1874",
        "end": "Aug. 16, 1878",
        "party": ["Liberal"]
    },
    {
        "number": 4,
        "begin": "Nov. 21, 1878",
        "end": "May 18, 1882",
        "party": ["Conservative"]
    },
    {
        "number": 5,
        "begin": "Aug. 7, 1882",
        "end": "Jan. 15, 1887",
        "party": ["Conservative"]
    },
    {
        "number": 6,
        "begin": "Apr. 13, 1887",
        "end": "Feb. 3, 1891",
        "party": ["Conservative"]
    },
    {
        "number": 7,
        "begin": "Apr. 7, 1891",
        "end": "Apr. 24, 1896",
        "party": ["Conservative"]
    },
    {
        "number": 8,
        "begin": "Jul. 13, 1896",
        "end": "Oct. 9, 1900",
        "party": ["Liberal"]
    },
    {
        "number": 9,
        "begin": "Dec. 5, 1900",
        "end": "Sep. 29, 1904",
        "party": ["Liberal"]
    },
    {
        "number": 10,
        "begin": "Dec. 15, 1904",
        "end": "Sep. 17, 1908",
        "party": ["Liberal"]
    },
    {
        "number": 11,
        "begin": "Dec. 3, 1908",
        "end": "Jul. 29, 1911",
        "party": ["Liberal"]
    },
    {
        "number": 12,
        "begin": "Oct. 7, 1911",
        "end": "Oct. 6, 1917",
        "party": ["Conservative"]
    },
    {
        "number": 13,
        "begin": "Mar. 16, 1918",
        "end": "Oct. 4, 1921",
        "party": ["Conservative"]
    },
    {
        "number": 14,
        "begin": "Jan. 15, 1922",
        "end": "Sep. 5, 1925",
        "party": ["Liberal"]
    },
    {
        "number": 15,
        "begin": "Dec. 7, 1925",
        "end": "Jul. 2, 1926",
        "party": ["Liberal","Conservative"]
    },
    {
        "number": 16,
        "begin": "Nov. 2, 1926",
        "end": "May 30, 1930",
        "party": ["Liberal"]
    },
    {
        "number": 17,
        "begin": "Aug. 18, 1930",
        "end": "Aug. 14, 1935",
        "party": ["Conservative"]
    },
    {
        "number": 18,
        "begin": "Nov. 9, 1935",
        "end": "Jan. 25, 1940",
        "party": ["Liberal"]
    },
    {
        "number": 19,
        "begin": "Apr. 17, 1940",
        "end": "Apr. 16, 1945",
        "party": ["Liberal"]
    },
    {
        "number": 20,
        "begin": "Aug. 9, 1945",
        "end": "Apr. 30, 1949",
        "party": ["Liberal"]
    },
    {
        "number": 21,
        "begin": "Aug. 29, 1949",
        "end": "Jun. 13, 1953",
        "party": ["Liberal"]
    },
    {
        "number": 22,
        "begin": "Oct. 8, 1953",
        "end": "Apr. 12, 1957",
        "party": ["Conservative"]
    },
    {
        "number": 23,
        "begin": "Aug. 8, 1957",
        "end": "Feb. 1, 1958",
        "party": ["Progressive Conservative"]
    },
    {
        "number": 24,
        "begin": "Apr. 30, 1958",
        "end": "Apr. 19, 1962",
        "party": ["Conservative Conservative"]
    },
    {
        "number": 25,
        "begin": "Jul. 18, 1962",
        "end": "Feb. 6, 1963",
        "party": ["Progressive Conservative"]
    },
    {
        "number": 26,
        "begin": "May 8, 1963",
        "end": "Sep. 8, 1965",
        "party": ["Liberal"]
    },
    {
        "number": 27,
        "begin": "Dec. 9, 1965",
        "end": "Apr. 23, 1968",
        "party": ["Liberal"]
    },
    {
        "number": 28,
        "begin": "Jul. 25, 1968",
        "end": "Sep. 1, 1972",
        "party": ["Liberal"]
    },
    {
        "number": 29,
        "begin": "Nov. 20, 1972",
        "end": "May 9, 1974",
        "party": ["Liberal"]
    },
    {
        "number": 30,
        "begin": "Jul. 31, 1974",
        "end": "Mar. 26, 1979",
        "party": ["Liberal"]
    },
    {
        "number": 31,
        "begin": "Jun. 11, 1979",
        "end": "Dec. 14, 1979",
        "party": ["Progressive Conservative"]
    },
    {
        "number": 32,
        "begin": "Mar. 10, 1980",
        "end": "Jul. 9, 1984",
        "party": ["Liberal"]
    },
    {
        "number": 33,
        "begin": "Sep. 24, 1984",
        "end": "Oct. 1, 1988",
        "party": ["Progressive Conservative"]
    },
    {
        "number": 34,
        "begin": "Dec. 12, 1988",
        "end": "Sep. 8, 1993",
        "party": ["Progressive Conservative"]
    },
    {
        "number": 35,
        "begin": "Nov. 15, 1993",
        "end": "Apr. 27, 1997",
        "party": ["Liberal"]
    },
    {
        "number": 36,
        "begin": "Jun. 23, 1997",
        "end": "Oct. 22, 2000",
        "party": ["Liberal"]
    },
    {
        "number": 37,
        "begin": "Dec. 18, 2000",
        "end": "May 23, 2004",
        "party": ["Liberal"]
    },
    {
        "number": 38,
        "begin": "Jul. 19, 2004",
        "end": "Nov. 29, 2005",
        "party": ["Liberal"]
    },
    {
        "number": 39,
        "begin": "Feb. 13, 2006",
        "end": "Sep. 7, 2008",
        "party": ["Conservative"]
    },
    {
        "number": 40,
        "begin": "Nov. 4, 2008",
        "end": "Mar. 26, 2011",
        "party": ["Conservative"]
    },
    {
        "number": 41,
        "begin": "May 23, 2011",
        "end": "Aug. 2, 2015",
        "party": ["Conservative"]
    },
    {
        "number": 42,
        "begin": "Dec. 3, 2015",
        "end": "present",
        "party": ["Liberal"]
    },
]

def get_date(d):
    y1 = int(d.split(",")[-1])
    m1 = int(
    {
        'Jan' : 1,
        'Feb' : 2,
        'Mar' : 3,
        'Apr' : 4,
        'May' : 5,
        'Jun' : 6,
        'Jul' : 7,
        'Aug' : 8,
        'Sep' : 9,
        'Oct' : 10,
        'Nov' : 11,
        'Dec' : 12
    }[d.split(",")[0].split(" ")[0].strip(".")])
    d1 = int(d.split(",")[0].split(" ")[-1])
    return date(y1, m1, d1)

def get_date_a(d):
    [y1, m1, d1] = [int(x) for x in d.split("-")]
    return date(y1, m1, d1)

"""
start
"""
df = read_data()
print(df.shape)
df = df.sort_values('speechdate',ascending=True)


periods_data = []

# historically get data for each period
ind = 0
term = parliament_terms[0]
begin = term["begin"]
d1 = get_date(begin)
end = term["end"]
d2 = get_date(end)
period_data = {
    "begin": begin,
    "end" : end,
    "data": pd.DataFrame()
}

row_ind = 0
# sum to check
sum_data = 0
while (ind<len(parliament_terms) and row_ind<df.shape[0]):
    row = df.iloc[row_ind]
    speech_date = row["speechdate"]
    speech_date_int = get_date_a(speech_date)
    # append to this period
    if (speech_date_int>=d1 and speech_date_int<d2):
        rows = period_data["data"]
        period_data["data"] = rows.append(row)
        row_ind = row_ind + 1
        print(row_ind)
        sum_data = sum_data+1
    # or other period
    # new period, new begin and end
    else:
        if period_data["data"].shape[0] > 0:
            period_data["data"].to_csv(str(d1)+"_"+str(d2)+".csv", sep='\t')
        periods_data.append(period_data)
        ind = ind + 1
        if(ind >= len(parliament_terms)):
           break
        term = parliament_terms[ind]
        begin = end
        d1 = d2
        end = term["end"]
        if(end=="present"):
            d2 = date.today()
        else:
            d2 = get_date(end)
        period_data = {
            "begin": begin,
            "end" : end,
            "data": pd.DataFrame()
        }

print(sum_data)
