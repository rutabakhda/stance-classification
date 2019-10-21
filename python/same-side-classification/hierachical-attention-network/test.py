"""
@author: Thang Nguyen <nhthang1009@gmail.com>
"""
import os
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
from src.utils import get_evaluation, exponent_neg_manhattan_distance
from src.dataset import MyDataset
import argparse
import shutil
import csv
import numpy as np


def get_args():
    parser = argparse.ArgumentParser(
        """Implementation of the model described in the paper: Hierarchical Attention Networks for Document Classification""")
    parser.add_argument("--batch_size", type=int, default=512)
    parser.add_argument("--data_path", type=str, default="data/test.csv")
    parser.add_argument("--pre_trained_model", type=str, default="trained_models/whole_model_han")
    parser.add_argument("--word2vec_path", type=str, default="data/glove.6B.50d.txt")
    parser.add_argument("--output", type=str, default="predictions")
    args = parser.parse_args()
    return args


def test(opt):
    test_params = {"batch_size": opt.batch_size,
                   "shuffle": False,
                   "drop_last": False}
    if os.path.isdir(opt.output):
        shutil.rmtree(opt.output)
    os.makedirs(opt.output)
    if torch.cuda.is_available():
        model = torch.load(opt.pre_trained_model)
    else:
        model = torch.load(opt.pre_trained_model, map_location=lambda storage, loc: storage)
    test_set = MyDataset(opt.data_path, opt.word2vec_path, model.max_sent_length, model.max_word_length)
    test_generator = DataLoader(test_set, **test_params)
    if torch.cuda.is_available():
        model.cuda()
    model.eval()
    te_label_ls = []
    te_pred_ls = []
    for te_feature1, te_feature2, te_label in test_generator:
        num_sample = len(te_label)
        print ("processing {} pairs".format(num_sample))
        if torch.cuda.is_available():
            te_feature1 = te_feature1.cuda()
            te_feature2 = te_feature2.cuda()
            te_label = te_label.cuda()
        with torch.no_grad():
            model._init_hidden_state(num_sample)
            te_feature1 = model(te_feature1)
            model._init_hidden_state(num_sample)
            te_feature2 = model(te_feature2)
        te_diff = exponent_neg_manhattan_distance(te_feature1, te_feature2)
        te_label_ls.extend(te_label.clone().cpu())
        te_pred_ls.append(te_diff.clone().cpu())
    te_pred = torch.cat(te_pred_ls, 0).numpy()
    te_label = np.array(te_label_ls)

    fieldnames = ['True label', 'Predicted label', 'Argument1', 'Argument2']
    with open(opt.output + os.sep + "predictions.csv", 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for i, j, k, l in zip(te_label, te_pred, test_set.texts_1, test_set.texts_2):
            if j >= 0.5:
                pred_lb = 1
            else:
                pred_lb = 0
            writer.writerow(
                {'True label': i, 'Predicted label': pred_lb, 'Argument1': k, 'Argument2': l})

    test_metrics = get_evaluation(te_label, te_pred,
                                  list_metrics=["accuracy", "confusion_matrix"])
    print("Prediction:\nAccuracy: {} \nConfusion matrix: \n{}".format(test_metrics["accuracy"],
                                                                               test_metrics["confusion_matrix"]))


if __name__ == "__main__":
    opt = get_args()
    test(opt)
