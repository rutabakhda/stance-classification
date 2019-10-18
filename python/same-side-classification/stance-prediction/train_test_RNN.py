"""
Step 4.2 / 5.2: Traing and Testing ""
"""

import torch
from torchtext import data

SEED = 1234
import pandas as pd
import numpy as np
torch.manual_seed(SEED)

torch.backends.cudnn.deterministic = True
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchtext

import nltk

import random
from sklearn.metrics import classification_report

import pyprind# get_ipython().run_line_magic('matplotlib', 'inline')

### preparing sheets
# for train, validation and test set from entire data,
# torchtext can load a custom dataset in csv and json.
# I chose csv for my convinience.

main_df = pd.read_csv("train.csv")
print(main_df.shape)
main_df = main_df.sample(n = main_df.shape[0])
main_df = main_df[["question_text", "target"]]
main_df.head()

# train_data
main_df.target.value_counts()
o_class = main_df.loc[main_df.target == 0,: ]
l_class = main_df.loc[main_df.target == 1,: ]

# preparing balanced test and validation set
number_o = o_class.shape[0]
number_l = l_class.shape[0]
#splitting test and train
test_o = o_class.iloc[: int(number_o/10),: ]
test_l = l_class.iloc[: int(number_l/10),: ]

valid_o = o_class.iloc[int(number_o/10): int(number_o/5),: ]
valid_l = l_class.iloc[int(number_l/10): int(number_l/5),: ]

train_o = o_class.iloc[int(number_o/5): ,: ]
train_l = l_class.iloc[int(number_l/5): ,: ]

train = pd.concat([train_o, train_l], axis = 0)
print(train.shape)

valid = pd.concat([valid_o, valid_l], axis = 0)
print(valid.shape)

test = pd.concat([test_o, test_l], axis = 0)
print(test.shape)

train.target.value_counts()

test.target.value_counts()

valid.target.value_counts()

# Saving files to disk

train.to_csv("torchtext_data/train.csv", index = False)
test.to_csv("torchtext_data/test.csv", index = False)
valid.to_csv("torchtext_data/valid.csv", index = False)

#freeing up some memory
del main_df, train, test, valid, train_l, train_o, test_l, test_o, valid_l, valid_o, o_class, l_class

# I am going to use spacy tokenizer.

import spacy
spacy_en = spacy.load('en')# nltk.download('punkt')

is_cuda = False

#### using torchtext to load text data

#sample tokenizer which you can use
def tokenizer(text):
  return [tok for tok in nltk.word_tokenize(text)]

# tokenizer = "spacy"
# uses spacy 's tokenizer
TEXT = data.Field(sequential = True, tokenize = "spacy")
LABEL = data.LabelField(sequential = False)

device = 'cpu'

#loading train, test and validation data
train_data, valid_data, test_data = data.TabularDataset.splits(
  path = "torchtext_data/", train = "train.csv",
  validation = "valid.csv", test = "test.csv", format = "csv", skip_header = True,
  fields = [('Text', TEXT), ('Label', LABEL)]
)

print(f'Number of training examples: {len(train_data)}')
print(f'Number of valid examples: {len(valid_data)}')
print(f'Number of testing examples: {len(test_data)}')

TEXT.build_vocab(train_data, vectors = torchtext.vocab.Vectors("glove.6B.300d.txt"),
    max_size = 20000, min_freq = 10)
LABEL.build_vocab(train_data)

#if you dont wanna load any word vectors# TEXT.build_vocab(train_data, max_size = 50000)# LABEL.build_vocab(train_data)

print(f"Unique tokens in TEXT vocabulary: {len(TEXT.vocab)}")
print(f"Unique tokens in LABEL vocabulary: {len(LABEL.vocab)}")

BATCH_SIZE = 2

device = 'cpu'

# keep in mind the sort_key option
train_iterator, valid_iterator, test_iterator = data.BucketIterator.splits(
  (train_data, valid_data, test_data), sort_key = lambda x: len(x.Text),
  batch_size = BATCH_SIZE,
  device = -1)

LABEL.vocab.freqs# torch.cuda.empty_cache()

class RNN(nn.Module):
    def __init__(self, input_dim, embedding_dim, hidden_dim, output_dim):
        super().__init__()

        self.embedding = nn.Embedding(input_dim, embedding_dim)
        self.rnn = nn.RNN(embedding_dim, hidden_dim) # also can use LSTM
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):

        #x = [sent len, batch size]

        embedded = self.embedding(x)

        #embedded = [sent len, batch size, emb dim]

        output, hidden = self.rnn(embedded)

        #output = [sent len, batch size, hid dim]
        #hidden = [1, batch size, hid dim]

        assert torch.equal(output[-1,:,:], hidden.squeeze(0))

        out = self.fc(hidden)
        return out

INPUT_DIM = len(TEXT.vocab)
EMBEDDING_DIM = 300
HIDDEN_DIM = 374
OUTPUT_DIM = 2

model = RNN(INPUT_DIM, EMBEDDING_DIM, HIDDEN_DIM, OUTPUT_DIM)

pretrained_embeddings = TEXT.vocab.vectors

print(pretrained_embeddings.shape)

model.embedding.weight.data = pretrained_embeddings

class_weights = torch.tensor([1.0, 15.0], device = device)

optimizer = optim.SGD(model.parameters(), lr = 1e-3)

criterion = nn.CrossEntropyLoss(weight = class_weights)

model = model.to(device)
criterion = criterion.to(device)

def binary_accuracy(preds, y):
    """
    Returns accuracy per batch, i.e. if you get 8/10 right, this returns 0.8, NOT 8
    """

    preds, ind= torch.max(F.softmax(preds, dim=-1), 1)
    correct = (ind == y).float()
    acc = correct.sum()/float(len(correct))
    return acc

def train(model, iterator, optimizer, criterion):

    epoch_loss = 0
    epoch_acc = 0

    model.train()
    bar = pyprind.ProgBar(len(iterator), bar_char='█')
    for batch in iterator:

        optimizer.zero_grad()

        predictions = model(batch.Text).squeeze(0)
#         print(predictions.shape, batch.Label.shape, model(batch.Text).shape)
        loss = criterion(predictions, batch.Label)
#         print(loss.shape)
        acc = binary_accuracy(predictions, batch.Label)

        loss.backward()

        optimizer.step()

        epoch_loss += loss.item()
        epoch_acc += acc.item()
        bar.update()
    return epoch_loss / len(iterator), epoch_acc / len(iterator)

def evaluate(model, iterator, criterion):

    epoch_loss = 0
    epoch_acc = 0

    model.eval()

    with torch.no_grad():
        bar = pyprind.ProgBar(len(iterator), bar_char='█')
        for batch in iterator:

            predictions = model(batch.Text).squeeze(0)

            loss = criterion(predictions, batch.Label)

            acc = binary_accuracy(predictions, batch.Label)

            epoch_loss += loss.item()
            epoch_acc += acc.item()
            bar.update()
    return epoch_loss / len(iterator), epoch_acc / len(iterator)

N_EPOCHS = 2

for epoch in range(N_EPOCHS):

    train_loss, train_acc = train(model, train_iterator, optimizer, criterion)
    valid_loss, valid_acc = evaluate(model, valid_iterator, criterion)

    print(f'| Epoch: {epoch+1:02} | Train Loss: {train_loss:.3f} | Train Acc: {train_acc*100:.2f}% | Val. Loss: {valid_loss:.3f} | Val. Acc: {valid_acc*100:.2f}% |')

test_loss, test_acc = evaluate(model, test_iterator, criterion)

print(f'| Test Loss: {test_loss:.3f} | Test Acc: {test_acc*100:.2f}% |')

def predict_sentiment(sentence):
    tokenized = [tok for tok in sentence.split()]
    indexed = [TEXT.vocab.stoi[t] for t in tokenized]
    tensor = torch.LongTensor(indexed).to(device)

    tensor = tensor.unsqueeze(1)
#     print(tensor.shape)
    prediction = model(tensor)
#     print(prediction)
    preds, ind= torch.max(F.softmax(prediction.squeeze(0), dim=-1), 1)
#     print(preds)
    return preds, ind

text = "My voice range is A2-C5. My chest voice goes up to F4. Included sample in my higher chest range. What is my voice type?"
predict_sentiment(text)[1].item()

# calculating classification report
test = pd.read_csv("torchtext_data/test.csv")

pre = [predict_sentiment(k)[1].item() for k in test.question_text]

print(classification_report(test.target, pre))

test_df = pd.read_csv("test.csv")
print(test_df.shape)# test_df = test_df.head(1000)

test_predictions = [int(predict_sentiment(k)[1].item()) for k in test_df.question_text]

out_df = pd.DataFrame({"qid":test_df["qid"].values})
out_df['prediction'] = test_predictions
print(out_df.shape)
out_df.head()

out_df.to_csv("submission.csv", index = False)

out_df.head()
