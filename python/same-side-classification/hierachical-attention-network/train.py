"""
@author: Thang Nguyen <nhthang1009@gmail.com>
"""
import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from src.utils import get_max_lengths, get_evaluation, exponent_neg_manhattan_distance
from src.dataset import MyDataset
from src.hierarchical_att_model import HierAttNet
from tensorboardX import SummaryWriter
import argparse
import shutil
import numpy as np


def get_args():
    parser = argparse.ArgumentParser(
        """Implementation of the model described in the paper: Hierarchical Attention Networks for Document Classification""")
    parser.add_argument("--batch_size", type=int, default=16)
    parser.add_argument("--num_epoches", type=int, default=30)
    parser.add_argument("--lr", type=float, default=0.01)
    parser.add_argument("--momentum", type=float, default=0.9)
    parser.add_argument("--word_hidden_size", type=int, default=50)
    parser.add_argument("--sent_hidden_size", type=int, default=50)
    parser.add_argument("--es_min_delta", type=float, default=0.0,
                        help="Early stopping's parameter: minimum change loss to qualify as an improvement")
    parser.add_argument("--es_patience", type=int, default=5,
                        help="Early stopping's parameter: number of epochs with no improvement after which training will be stopped. Set to 0 to disable this technique.")
    parser.add_argument("--train_set", type=str, default="data/train.csv")
    parser.add_argument("--test_set", type=str, default="data/test.csv")
    parser.add_argument("--test_interval", type=int, default=1, help="Number of epoches between testing phases")
    parser.add_argument("--word2vec_path", type=str, default="data/glove.6B.50d.txt")
    parser.add_argument("--log_path", type=str, default="tensorboard/han_voc")
    parser.add_argument("--saved_path", type=str, default="trained_models")
    args = parser.parse_args()
    return args


def train(opt):
    if torch.cuda.is_available():
        torch.cuda.manual_seed(123)
    else:
        torch.manual_seed(123)
    output_file = open(opt.saved_path + os.sep + "logs.txt", "w")
    output_file.write("Model's parameters: {}".format(vars(opt)))
    training_params = {"batch_size": opt.batch_size,
                       "shuffle": True,
                       "drop_last": True}
    test_params = {"batch_size": opt.batch_size,
                   "shuffle": False,
                   "drop_last": False}

    max_word_length, max_sent_length = get_max_lengths(opt.train_set)
    training_set = MyDataset(opt.train_set, opt.word2vec_path, max_sent_length, max_word_length)
    training_generator = DataLoader(training_set, **training_params)
    test_set = MyDataset(opt.test_set, opt.word2vec_path, max_sent_length, max_word_length)
    test_generator = DataLoader(test_set, **test_params)

    model = HierAttNet(opt.word_hidden_size, opt.sent_hidden_size, opt.batch_size, training_set.num_classes,
                       opt.word2vec_path, max_sent_length, max_word_length)


    if os.path.isdir(opt.log_path):
        shutil.rmtree(opt.log_path)
    os.makedirs(opt.log_path)
    writer = SummaryWriter(opt.log_path)
    # writer.add_graph(model, torch.zeros(opt.batch_size, max_sent_length, max_word_length))

    if torch.cuda.is_available():
        model.cuda()

    criterion = nn.MSELoss()
    optimizer = torch.optim.SGD(filter(lambda p: p.requires_grad, model.parameters()), lr=opt.lr, momentum=opt.momentum)
    # optimizer = torch.optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=opt.lr)
    best_loss = 1e5
    best_epoch = 0
    model.train()
    num_iter_per_epoch = len(training_generator)
    for epoch in range(opt.num_epoches):
        for iter, (feature1, feature2, label) in enumerate(training_generator):
            if torch.cuda.is_available():
                feature1 = feature1.cuda()
                feature2 = feature2.cuda()
                label = label.cuda()
            optimizer.zero_grad()
            model._init_hidden_state()
            feature1 = model(feature1)
            model._init_hidden_state()
            feature2 = model(feature2)

            diff = exponent_neg_manhattan_distance(feature1, feature2)
            loss = criterion(diff, label.float())
            loss.backward()
            optimizer.step()
            training_metrics = get_evaluation(label.cpu().numpy(), diff.cpu().detach().numpy(), list_metrics=["accuracy"])
            print("Epoch: {}/{}, Iteration: {}/{}, Lr: {}, Loss: {}, Accuracy: {}".format(
                epoch + 1,
                opt.num_epoches,
                iter + 1,
                num_iter_per_epoch,
                optimizer.param_groups[0]['lr'],
                loss, training_metrics["accuracy"]))
            writer.add_scalar('Train/Loss', loss, epoch * num_iter_per_epoch + iter)
            writer.add_scalar('Train/Accuracy', training_metrics["accuracy"], epoch * num_iter_per_epoch + iter)
        # torch.save(model, opt.saved_path + os.sep + "whole_model_han_{}".format(epoch))
        if epoch % opt.test_interval == 0:
            model.eval()
            loss_ls = []
            te_label_ls = []
            te_pred_ls = []
            for te_feature1, te_feature2, te_label in test_generator:
                num_sample = len(te_label)
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
                te_loss = criterion(te_diff, te_label.float())
                loss_ls.append(te_loss * num_sample)
                te_label_ls.extend(te_label.clone().cpu())
                te_pred_ls.append(te_diff.clone().cpu())
            te_loss = sum(loss_ls) / test_set.__len__()
            te_pred = torch.cat(te_pred_ls, 0)
            te_label = np.array(te_label_ls)
            test_metrics = get_evaluation(te_label, te_pred.numpy(), list_metrics=["accuracy", "confusion_matrix"])
            output_file.write(
                "Epoch: {}/{} \nTest loss: {} Test accuracy: {} \nTest confusion matrix: \n{}\n\n".format(
                    epoch + 1, opt.num_epoches,
                    te_loss,
                    test_metrics["accuracy"],
                    test_metrics["confusion_matrix"]))
            print("Epoch: {}/{}, Lr: {}, Loss: {}, Accuracy: {}".format(
                epoch + 1,
                opt.num_epoches,
                optimizer.param_groups[0]['lr'],
                te_loss, test_metrics["accuracy"]))
            writer.add_scalar('Test/Loss', te_loss, epoch)
            writer.add_scalar('Test/Accuracy', test_metrics["accuracy"], epoch)
            model.train()
            if te_loss + opt.es_min_delta < best_loss:
                best_loss = te_loss
                best_epoch = epoch
                torch.save(model, opt.saved_path + os.sep + "whole_model_han")

            # Early stopping
            if epoch - best_epoch > opt.es_patience > 0:
                print("Stop training at epoch {}. The lowest loss achieved is {}".format(epoch, te_loss))
                break


if __name__ == "__main__":
    opt = get_args()
    train(opt)
