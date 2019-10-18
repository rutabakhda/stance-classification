from helper_argsme_train_test_similarity import *

"""
Step 3: Train and Test using Similarity
Divide the argsme claims into training and testing
Using similarity comparison to train and test
Visualize the results
"""

if __name__=="__main__":
    # read csv all claims
    df = read_csv("../data/argsme_all_claims_abortion/argsme_all_claims_abortion.csv")
    # divide into training and test, not saved
    (df_training, df_test) = divide_df(df, 0.2, False)
    # get for and against claims from training df and rank them
    (training_for_arguments, training_against_arguments) = get_for_against_claims(df_training)
    training_for_arguments = rank_arguments(training_for_arguments)
    training_against_arguments = rank_arguments(training_against_arguments)
    # write ranked for and against claims to file
    write_list_to_file("../data/argsme_training_arguments/for_arguments.txt", training_for_arguments)
    write_list_to_file("../data/argsme_training_arguments/against_arguments.txt", training_against_arguments)
    # test and save into [index, text, stance, predicted] format
    confusion_matrix = test_arguments_similarity("../data/argsme_test_arguments_results/overall_similarity.csv", (training_for_arguments, training_against_arguments), df_test,
                              "../data/argsme_test_arguments_results/sentence_similarity.csv")
    # plot confusion matrix & accuracy
    plot_confusion_matrix(confusion_matrix,normalize=False,classes=["for","against"],title="Confusion matrix")
    plot_accuracy(confusion_matrix)
