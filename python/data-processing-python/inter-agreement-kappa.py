from sklearn.metrics import cohen_kappa_score

f1 = open("ruta.txt", "r")
rater1 = []
for x1 in f1:
     label1 = x1.split("=", 1)[1]
     label1 = label1.strip('\n')
     rater1.append(label1)

f2 = open("weifan.txt", "r")
rater2 = []
for x2 in f2:
    label2 = x2.split("=", 1)[1]
    label2 = label2.strip('\n')
    rater2.append(label2)

f3 = open("yamen.txt", "r")
rater3 = []
for x3 in f3:
    label3 = x3.split("=", 1)[1]
    label3 = label3.strip('\n')
    rater3.append(label3)

f4 = open("lukas.txt", "r")
rater4 = []
for x4 in f4:
    label4 = x4.split("=", 1)[1]
    label4 = label4.strip('\n')
    rater4.append(label4)

f5 = open("annie.txt", "r")
rater5 = []
for x5 in f5:
    label5 = x5.split("=", 1)[1]
    label5 = label5.strip('\n')
    rater5.append(label5)

print(len(rater1))
print(len(rater2))
print(len(rater3))
print(len(rater4))
print(len(rater5))
print("cohen kappa score")
print(cohen_kappa_score(rater1, rater2,rater3))

