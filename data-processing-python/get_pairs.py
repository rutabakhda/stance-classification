import csv
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import glob
import errno
import os
import natsort

"""
Process data of same period and topic based on the political party
"""

def nCr(n,r):
    f = math.factorial
    return f(n) // f(r) // f(n-r)

# read the folders with csv files
path = 'dataset_by-period_by-topic/*.csv'
files = glob.glob(path)
# sort file from old to new speeches
files = natsort.natsorted(files)
statistics_each_period = []

# statistics
count = 0
sum_pairs = 0
sum_positive_pairs = 0

d1 = "positive_pairs"
if not os.path.exists(d1):
    os.makedirs(d1)

d2 = "negative_pairs"
if not os.path.exists(d2):
    os.makedirs(d2)

for name in files:
    try:
        with open(name) as f:
            # get data from file
            df = pd.read_csv(name, sep='\t', index_col=0)
            file_name = name.split("/")[-1].strip(".csv")
            print(file_name)

            # sum statistics of file and number of pairs
            rows = df.shape[0]
            print("rows", rows)
            pairs = nCr(rows, 2)
            sum_pairs = sum_pairs + pairs
            # positive pairs
            positive_pairs = 0
            df1 = df.groupby("Role")['basepk'].nunique().reset_index()
            df1 = df1.sort_values(by="basepk")
            no_same_party_speeches = df1["basepk"].tolist()
            for no_speeches in no_same_party_speeches:
                if(no_speeches > 1):
                    positive_pairs = positive_pairs + nCr(no_speeches, 2)
            sum_positive_pairs = sum_positive_pairs + positive_pairs
            print(pairs, positive_pairs, pairs-positive_pairs)

            # get pairs of speeches and save them
            for ind1 in range(df.shape[0]):
                ind2 = ind1 + 1
                row1 = df.iloc[ind1]
                while ind2 < df.shape[0]:
                    row2 = df.iloc[ind2]
                    df2 = pd.DataFrame(columns=df.columns)
                    df2 = df2.append(row1,ignore_index=True)
                    df2 = df2.append(row2,ignore_index=True)
                    is_positive = row1["Role"] is row2["Role"]
                    folder_name = "positive_pairs" if is_positive else "negative_pairs"
                    period = ("_").join(file_name.split("_")[:-1])
                    topic_name = file_name.split("_")[-1]
                    df2.to_csv(folder_name + "/" + period + "_" + format(count, '05d') + "_" + topic_name + ".csv")
                    ind2 = ind2 + 1
                    count = count + 1
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise

print(count)
print("sum_pairs", sum_pairs)
print("positive_pairs", sum_positive_pairs)
print("negavtive_pairs", sum_pairs - sum_positive_pairs)

"""
Sum statistics about files and number of pairs
2004-05-23_2005-11-29_Sponsorship Program.csv
rows 12
66 55 11
1993-09-08_1997-04-27_Gun Control.csv
rows 57
1596 784 812
1997-04-27_2000-10-22_Election Campaign In Quebec.csv
rows 24
276 276 0
1993-09-08_1997-04-27_Justice.csv
rows 35
595 379 216
2000-10-22_2004-05-23_Health Care.csv
rows 29
406 202 204
1997-04-27_2000-10-22_Health Care.csv
rows 36
630 387 243
2000-10-22_2004-05-23_Health.csv
rows 55
1485 785 700
1993-09-08_1997-04-27_National Unity.csv
rows 45
990 574 416
2005-11-29_2008-09-07_Aboriginal Affairs.csv
rows 22
231 159 72
2005-11-29_2008-09-07_Government Policies.csv
rows 24
276 148 128
2000-10-22_2004-05-23_Violence Against Women.csv
rows 26
325 165 160
2004-05-23_2005-11-29_International Women's Day.csv
rows 12
66 34 32
2005-11-29_2008-09-07_The Environment.csv
rows 38
703 367 336
2004-05-23_2005-11-29_Status of Women.csv
rows 10
45 24 21
2011-03-26_2015-08-02_New Democratic Party of Canada.csv
rows 124
7626 6486 1140
2005-11-29_2008-09-07_Government Programs.csv
rows 18
153 121 32
1993-09-08_1997-04-27_The Economy.csv
rows 28
378 186 192
1997-04-27_2000-10-22_Hepatitis C.csv
rows 38
703 598 105
1993-09-08_1997-04-27_Referendum Campaign.csv
rows 52
1326 686 640
1993-09-08_1997-04-27_Health Care.csv
rows 43
903 443 460
2005-11-29_2008-09-07_The Budget.csv
rows 48
1128 616 512
2008-09-07_2011-03-26_Bloc Québécois.csv
rows 29
406 406 0
2005-11-29_2008-09-07_Liberal Party of Canada.csv
rows 21
210 172 38
2004-05-23_2005-11-29_Violence Against Women.csv
rows 15
105 49 56
2005-11-29_2008-09-07_Bloc Québécois.csv
rows 23
253 231 22
1993-09-08_1997-04-27_Taxation.csv
rows 39
741 391 350
2008-09-07_2011-03-26_The Budget.csv
rows 36
630 355 275
2008-09-07_2011-03-26_The Economy.csv
rows 88
3828 2916 912
2004-05-23_2005-11-29_The Budget.csv
rows 12
66 30 36
2011-03-26_2015-08-02_Leader of the Liberal Party of Canada.csv
rows 39
741 571 170
2008-09-07_2011-03-26_Status of Women.csv
rows 49
1176 816 360
1997-04-27_2000-10-22_The Senate.csv
rows 33
528 528 0
2008-09-07_2011-03-26_Firearms Registry.csv
rows 25
300 144 156
2000-10-22_2004-05-23_Terrorism.csv
rows 45
990 514 476
2004-05-23_2005-11-29_Health.csv
rows 24
276 136 140
1997-04-27_2000-10-22_Aboriginal Affairs.csv
rows 23
253 193 60
2011-03-26_2015-08-02_International Trade.csv
rows 40
780 636 144
2005-11-29_2008-09-07_Human Rights.csv
rows 20
190 94 96
1997-04-27_2000-10-22_Taxation.csv
rows 48
1128 993 135
1993-09-08_1997-04-27_Quebec Sovereignty.csv
rows 29
406 216 190
2000-10-22_2004-05-23_Agriculture.csv
rows 101
5050 3150 1900
1993-09-08_1997-04-27_Violence Against Women.csv
rows 47
1081 661 420
1997-04-27_2000-10-22_Agriculture.csv
rows 56
1540 1012 528
2000-10-22_2004-05-23_Taxation.csv
rows 22
231 174 57
2011-03-26_2015-08-02_Violence Against Women.csv
rows 67
2211 1199 1012
2011-03-26_2015-08-02_Taxation.csv
rows 214
22791 11391 11400
2000-10-22_2004-05-23_Human Rights.csv
rows 22
231 119 112
1997-04-27_2000-10-22_The Budget.csv
rows 25
300 150 150
2000-10-22_2004-05-23_Middle East.csv
rows 26
325 157 168
2000-10-22_2004-05-23_The Environment.csv
rows 39
741 391 350
1997-04-27_2000-10-22_Violence Against Women.csv
rows 40
780 480 300
1988-10-01_1993-09-08_PETITIONS.csv
rows 9
36 28 8
2008-09-07_2011-03-26_Employment Insurance.csv
rows 21
210 106 104
2011-03-26_2015-08-02_Leader of the New Democratic Party of Canada.csv
rows 40
780 741 39
2008-09-07_2011-03-26_Taxation.csv
rows 61
1830 1406 424
2004-05-23_2005-11-29_Foreign Affairs.csv
rows 10
45 20 25
1993-09-08_1997-04-27_Quebec Referendum.csv
rows 54
1431 766 665
2005-11-29_2008-09-07_Status of Women.csv
rows 53
1378 982 396
2004-05-23_2005-11-29_Justice.csv
rows 11
55 45 10
2008-09-07_2011-03-26_Liberal Party of Canada.csv
rows 52
1326 1179 147
2011-03-26_2015-08-02_Justice.csv
rows 30
435 291 144
1997-04-27_2000-10-22_Health.csv
rows 23
253 133 120
2000-10-22_2004-05-23_Softwood Lumber.csv
rows 21
210 130 80
2011-03-26_2015-08-02_The Budget.csv
rows 34
561 273 288
2008-09-07_2011-03-26_Justice.csv
rows 44
946 751 195
2004-05-23_2005-11-29_Agriculture.csv
rows 44
946 658 288
2005-11-29_2008-09-07_Carbon Tax Proposal.csv
rows 26
325 256 69
2008-09-07_2011-03-26_Leader of the Liberal Party of Canada.csv
rows 60
1770 1654 116
2011-03-26_2015-08-02_Status of Women.csv
rows 52
1326 686 640
2011-03-26_2015-08-02_The Economy.csv
rows 73
2628 1946 682
2004-05-23_2005-11-29_Pope John Paul II.csv
rows 12
66 30 36
sum_pairs 84752
positive_pairs 53831 => 56786
negavtive_pairs 30921 => 27966
"""
