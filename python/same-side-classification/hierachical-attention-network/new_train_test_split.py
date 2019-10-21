import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("data/new_test.csv", header=0)
label = df["is_same_side"]
X_train, X_test, y_train, y_test = train_test_split(df, label, test_size=0.2, stratify=label)
X_train.to_csv("data/new_train.csv", header = ["argument1", "argument2", "is_same_side"], sep = "\t", index=False)
X_test.to_csv("data/new_test.csv", header = ["argument1", "argument2", "is_same_side"], sep = "\t", index=False)
df.to_csv("data/new_full.csv", header = ["argument1", "argument2", "is_same_side"], sep = "\t", index=False)