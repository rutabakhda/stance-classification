import pandas as pd
from sklearn.model_selection import train_test_split

label_converter = lambda x: 1 if x == "True" else 0
text_converter = lambda x: x.lower()
df = pd.read_csv("data/input.csv", sep=',', converters={"argument1": text_converter, "argument2": text_converter,
                                                          "is_same_side": label_converter}, escapechar="\\", header=0,
                   usecols=["argument1", "argument2", "is_same_side"])
label = df["is_same_side"]

X_train, X_test, y_train, y_test = train_test_split(df, label, test_size=0.2, stratify=label)
X_train.to_csv("data/train.csv", header = ["argument1", "argument2", "is_same_side"], sep = "\t", index=False)
X_test.to_csv("data/test.csv", header = ["argument1", "argument2", "is_same_side"], sep = "\t", index=False)