import csv
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""
Statistics about frequencies parties giving speeches
"""

def read_data():
    with open("dataset/labelled-statement-by-members.csv") as f:
        reader = csv.DictReader(f)
        data = [r for r in reader]
    # print(json.dumps(data[-1], indent=4, sort_keys=True))

    df = pd.DataFrame.from_dict(data)
    df = df.replace({"Bloc":"Bloc Québécois"})
    df = df.replace({"GPQ (ex-Bloc)":"Québec debout"})
    df = df.replace({"NDP":"New Democratic Party"})
    df = df.replace({"Green":"Green Party"})

    return df

df = read_data()
df1 = df.groupby("speakerparty")['basepk'].nunique().reset_index()
df1 = df1.sort_values(by="basepk")
# print(df1)
# print("sum: ",df1["basepk"].sum()) #21332

df2 = df.groupby("Role")['basepk'].nunique().reset_index()
df2 = df2.sort_values(by="basepk")
# print(df2)

# drawing
n = df1.shape[0]
fig, ax = plt.subplots()
ax.bar(range(n), df1["basepk"], width=1, align='center')
ax.set(xticks=range(n), xlim=[-1, n])
ax.set_xticklabels(df1["speakerparty"])
plt.xticks(rotation=90)
# plt.show()

"""
Remarks:
https://en.wikipedia.org/wiki/Qu%C3%A9bec_debout
this party: Québec debout or  Quebec Parliamentary Group (QPG)
consists of memebers that resigned from Bloc Québécois
who resigned due to their opposition to the leadership.
founded: February 28, 2018
dissolved: September 17, 2018

Remarks:
these are political parties in canada
https://en.wikipedia.org/wiki/List_of_federal_political_parties_in_Canada

Remarks:
this is a list of canadian parliaments
https://en.wikipedia.org/wiki/List_of_Canadian_federal_parliaments
=> most of the speeches come from government (liberal and conservative)
                speakerparty  basepk
3       Forces et Démocratie       2
11                       nan       4
9              Québec debout      14
4                Green Party      15
5                Independent      61
8   Progressive Conservative     370
1          Canadian Alliance     681
10                    Reform    1271
7       New Democratic Party    2606
0             Bloc Québécois    3536
2               Conservative    4980
6                    Liberal    7792

=> We have quite balance numbers of government and opposition (in total) speeches
         Role  basepk
2     Unknown       4
0  Government    9994 (47%)
1  Opposition   11334 (53%)

We have data from 1994 to 2017: 24 years / 4 = approx. 6 parliaments' terms
[
    {
        "Role": "Government",
        "basepk": "3970005",
        "speakername": "Roseanne Skoke",
        "speakerparty": "Liberal",
        "speechdate": "1994-06-10",
        "speechtext": "I commend to the House private member's Bill C-235, an act to amend the Criminal Code relevant to the issue of abortion introduced by the hon. member for Glengarry-Prescott-Russell.\n The purpose of the bill is to make it a criminal offence to require a physician, nurse, staff member or employee of a hospital or health facility to perform or participate in an abortion procedure.\n The bill would also make it a criminal offence to discriminate against any of these persons for refusing to perform or participate in an abortion procedure.\n It is time Parliament exercised its jurisdiction to enact legislation to protect and safeguard the rights and life of a child ventre sa mere, the child within the womb.\n Enact legislation now to guarantee the right to life at all stages from the moment of conception until natural death.",
        "subtopic": "Right To Life"
    },
    ...
    {
        "Role": "Opposition",
        "basepk": "4728198",
        "speakername": "Deepak Obhrai",
        "speakerparty": "Conservative",
        "speechdate": "2017-11-22",
        "speechtext": "for Zimbabwe and Africa, the resignation of Robert Mugabe is excellent news.\n  Having been born in Africa, I witnessed the winds of change blowing. At independence for the people of Zimbabwe, a new era of hope and prosperity was in the offing, but Mugabe's subsequent abuses of human rights and crimes turned those hopes around quickly into an dictatorial regime, drowning in poverty. \n I met with the official opposition leader, Morgan Tsvangirai, when he visited Canada and discussed extensively our shared hopes for a democratic future for Zimbabwe. It has been a long journey but today that hope has returned.\n  We will support the people of Zimbabwe in the bright future ahead of them. Good luck to Zimbabweans.",
        "subtopic": "Zimbabwe"
    }
]

Remarks of parties' foundation and dissolvation

- Progressive Conservative Party
The first Conservative Party used several different names during its existence:

Liberal-Conservative Party (some MPs until 1911),
Unionist Party (1917-1921),
National Liberal and Conservative Party (1920-1921),
National Government (1940),
Progressive Conservative Party (1942-2003)

- The party Unionist coalition exists during (1918–1920)
https://en.wikipedia.org/wiki/Unionist_Party_(Canada)
and later named National Liberal and Conservative Party (1920–1921)

- Reform party is succeeded by Canadian Alliance
https://en.wikipedia.org/wiki/Reform_Party_of_Canada

- Progressive Conservative Party: according to
https://en.wikipedia.org/wiki/Progressive_Conservative_Party_of_Canada#History
this party is founded in 1942 and dissolved in 2003 to
merge with Canadian Alliance party to form the mordern Conservative Party
"""

"""
Remarks: Earliest speeches are from 1994
Split to durations based on
https://en.wikipedia.org/wiki/List_of_Canadian_federal_parliaments
"""
