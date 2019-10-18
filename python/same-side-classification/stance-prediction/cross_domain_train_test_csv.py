from argsme_train_test_csv import *

"""
Step 5.2: Generate cross-domain
training with argsme data
and testing with parliament data
"""

def generate_train_csv_argsme():
    """
    Read the dataset from 5.1
    and write to train.csv
    """
    df = read_csv("../data/argsme_all_claims_abortion/argsme_all_claims_abortion.csv")
    # method 1: train and test using each sentence
    # (for_arguments, against_arguments) = get_for_against_claims(df)
    # method 2: train and test using full argument
    (for_arguments, against_arguments) = get_for_against_arguments(df)
    # for_arguments = clean_data_2(for_arguments)
    # against_arguments = clean_data_2(against_arguments)
    df1 = create_df(for_arguments, "for")
    df0 = create_df(against_arguments, "against")
    df = pd.concat([df1, df0], axis=0)
    df = df.sample(frac=1).reset_index(drop=True)
    # drop rows contain empty string
    filter = df["question_text"] != ""
    df = df[filter]
    df.to_csv(r"train.csv")

def generate_test_csv_parliament():
    """
    Read the dataset from step 5.1
    and write to test.csv
    """
    df = pd.read_csv("../data/parliament_all_abortion_statements/parliament_abortion.csv")
    # print(df)
    df = df.loc[(df.stance == 0) | (df.stance == 1)]
    df = df.rename(columns={'stance': 'target', 'summary': 'question_text'})
    df["question_text"] = df['question_text'].apply(lambda x: ". ".join(ast.literal_eval(x)))
    df = df.filter(["basepk", "question_text", "target"])
    df.to_csv(r"test.csv")

if __name__=="__main__":
    generate_train_csv_argsme()
    generate_test_csv_parliament()
