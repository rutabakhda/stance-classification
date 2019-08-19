import csv
import json
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import glob
import errno


"""
Divide data in same periods to different topics
"""

"""
start
"""

def divide(df, file_name):
    df1 = df.groupby("subtopic")['basepk'].nunique().reset_index()
    df1 = df1.sort_values(by="basepk")
    print(df.shape)
    print(df1)
    # number of speeches for this specific periods
    no_speeches = df1['basepk'].tolist()
    # only get the topic of the n most frequent topics
    n = 10
    topics = ["" for x in range(len(no_speeches) - n)] + df1['subtopic'].tolist()[-n:]
    period = file_name

    # save speeches in same topic to file
    term = file_name.split("/")[-1].strip(".csv")
    for topic in df1['subtopic'].tolist()[-n:]:
        df_topic = df[df['subtopic']==topic]
        df_topic.to_csv(term+"_"+topic+".csv", sep='\t')
    return (no_speeches, topics, period)

mpl.rcParams['font.size'] = 5.5
def plot_chart(results):
    for result in results:
        fig = plt.figure()
        plt.pie(result[0], labels=result[1])
        fig.suptitle(result[2], fontsize = 16)
        fig.savefig(result[2].replace("csv","png"), dpi=300)
    plt.show()

# read the folders with csv files
path = 'dataset_by-period/*.csv'
files = glob.glob(path)
# data statistics
statistics_each_period = []
for name in files:
    print(name)
    try:
        with open(name) as f:
            # get data from file
            df = pd.read_csv(name, sep='\t', index_col=0)
            file_name = name.split("/")[-1]
            # divide by topic
            statistics_each_period.append(divide(df, name))
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise

# plot_chart(statistics_each_period)

"""
Results:
dataset_by-period/2008-09-07_2011-03-26.csv
(2287, 7)
                                   subtopic  basepk
0                            100th Birthday       1
792                       Museums in Canada       1
793                       My Sisters' Place       1
794                       NDP Deputy Leader       1
795                             Nancy Guyon       1
...                                     ...     ...
1093                        Status of Women      49
689                 Liberal Party of Canada      52
674   Leader of the Liberal Party of Canada      60
1115                               Taxation      61
1135                            The Economy      88

[1277 rows x 2 columns]
dataset_by-period/2000-10-22_2004-05-23.csv
(3069, 7)
                                               subtopic  basepk
0     15th Annual Fondation Mirella & Lino Saputo Go...       1
999                        National AIDS Awareness Week       1
997                         NATO Parliamentary Assembly       1
996                              NATO Jet Pilot Program       1
995                                    Mérite Stellaris       1
...                                                 ...     ...
632                                         Health Care      29
1422                                    The Environment      39
1414                                          Terrorism      45
631                                              Health      55
35                                          Agriculture     101

[1621 rows x 2 columns]
dataset_by-period/1988-10-01_1993-09-08.csv
(10, 7)
    subtopic  basepk
0  PETITIONS       9
dataset_by-period/2004-05-23_2005-11-29.csv
(1168, 7)
                                           subtopic  basepk
0    150th Anniversary of the Town of Saint-Sauveur       1
459                        National Day of Mourning       1
460                                National Defence       1
461                         National Highway System       1
462                               National Programs       1
..                                              ...     ...
614                             Sponsorship Program      12
644                                      The Budget      12
696                          Violence Against Women      15
288                                          Health      24
23                                      Agriculture      44

[744 rows x 2 columns]
dataset_by-period/1993-09-08_1997-04-27.csv
(3543, 7)
                             subtopic  basepk
0         12Th Regiment Of Valcartier       1
1145  Port Williams Elementary School       1
1144           Port Perry Cadet Corps       1
1143           Port Of Trois-Rivières       1
1141           Policy On Bilingualism       1
...                               ...     ...
1016                   National Unity      45
1717           Violence Against Women      47
1272              Referendum Campaign      52
1223                Quebec Referendum      54
655                       Gun Control      57

[1821 rows x 2 columns]
dataset_by-period/2011-03-26_2015-08-02.csv
(3653, 7)
                                          subtopic  basepk
0     15th Annual International Folklore Avalanche       1
1199               Organization for Homeless Youth       1
1196                       Orangeville Rotary Club       1
1195                        Orangeville Lions Club       1
1194           Orangeville Blues and Jazz Festival       1
...                                            ...     ...
1571                               Status of Women      52
1748                        Violence Against Women      67
1641                                   The Economy      73
1144                New Democratic Party of Canada     124
1615                                      Taxation     214

[1890 rows x 2 columns]
dataset_by-period/1997-04-27_2000-10-22.csv
(3007, 7)
                              subtopic  basepk
0          'Twas The Night After Kyoto       1
1004     Ordre Du Mérite Agricole 1999       1
1003  Opération Enfant Soleil Telethon       1
1002                        Opposition       1
1001               Operation Blue Star       1
...                                ...     ...
582                        Health Care      36
586                        Hepatitis C      38
1515            Violence Against Women      40
1342                          Taxation      48
31                         Agriculture      56

[1613 rows x 2 columns]
dataset_by-period/2005-11-29_2008-09-07.csv
(2253, 7)
                                               subtopic  basepk
0                    100th Birthday of Salvador Allende       1
847                              Official Languages Act       1
845   Official Development Assistance Accountability...       1
844                                  Oak Ridges—Markham       1
843                                Nutritional Medicine       1
...                                                 ...     ...
462                                 Government Policies      24
214                                 Carbon Tax Proposal      26
1177                                    The Environment      38
1171                                         The Budget      48
1135                                    Status of Women      53

[1330 rows x 2 columns]
"""
