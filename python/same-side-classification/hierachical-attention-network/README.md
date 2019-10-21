# [PYTORCH] Hierarchical Attention Networks for Same Side Classification

## Introduction

Here is my pytorch implementation of the model described in the paper **Hierarchical Attention Networks for Document Classification** [paper](https://www.cs.cmu.edu/~hovy/papers/16HLT-hierarchical-attention-networks.pdf). 



## How to use my code

With my code, you can:
* **Train your model with any dataset**
* **Given either my trained model or yours, you could evaluate any test dataset whose have the same set of classes**
* **Run a simple web app for testing purpose**

## Requirements:

* **python 3.6**
* **pytorch 0.4**
* **tensorboard**
* **tensorboardX** (This library could be skipped if you do not use SummaryWriter)
* **numpy**


If you want to train a model with default parameters, you could run:
- **python train.py**

If you want to train a model with your preference parameters, like optimizer and learning rate, you could run:
- **python train.py --batch_size batch_size --lr learning_rate**: For example, python train.py --batch_size 512 --lr 0.01

If you want to train a model with your preference word2vec model, you could run:
- **python train.py --word2vec_path path/to/your/word2vec**

## Test

For testing a trained model with your test file, please run the following command:
- **python test.py --word2vec_path path/to/your/word2vec**, with the word2vec file is the same as the one you use in training phase.



