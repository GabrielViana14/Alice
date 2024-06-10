import numpy as np
import random 
import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from nltk_utils import NltkUtils
from model.NeuralNet import NeuralNet

nltkutils = NltkUtils()


with open('machine_learning/intents/ptbr/intents.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)

all_words = []
tags = []
xy = []

#loopa para cada sentença dentro do intents "patterns"
for intent in intents['intents']:
    tag = intent['tag']
    #adicionar a lista de tag
    tags.append(tag)
    for pattern in intent['patterns']:
        # tokenize cada palavra na sentença
        w = nltkutils.tokenize(pattern)
        # adiciona a nossa lista de palavras
        all_words.extend(w)
        # adiciona ao par xy
        xy.append((w,tag))

# stem e lower em cada palavra
ignore_words = ['?','!',".",","]
all_words = [nltkutils.stem(w) for w in all_words if w not in ignore_words]
# remove duplicados e ordena
all_words = sorted(set(all_words))
tags = sorted(set(tags))

#criando os dados de treino
X_train = []
y_train = []
for (pattern_sentence, tag) in xy:
    # X: pacote de palavras para cada pattern_sentence
    bag = nltkutils.bag_of_words(pattern_sentence,all_words)
    X_train.append(bag)
    # y: PyTorch CrossEntropyLoss needs only class labels, not one-hot
    label = tags.index(tag)
    y_train.append(label)

X_train = np.array(X_train)
y_train = np.array(y_train)

# Hyper-parameters 
num_epochs = 1000
batch_size = 8
learning_rate = 0.001
input_size = len(X_train[0])
hidden_size = 8
output_size = len(tags)

class ChatDataset(Dataset):

    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    # support indexing such that dataset[i] can be used to get i-th sample
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    # we can call len(dataset) to return the size
    def __len__(self):
        return self.n_samples

dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset,
                          batch_size=batch_size,
                          shuffle=True,
                          num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = NeuralNet(input_size, hidden_size, output_size).to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Train the model
for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(device, dtype=torch.long)

        # Forward pass
        outputs = model(words)
        # if y would be one-hot, we must apply
        # labels = torch.max(labels, 1)[1]
        loss = criterion(outputs, labels)

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch+1) % 100 == 0:
        print (f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')


print(f'final loss: {loss.item():.4f}')

data = {
"model_state": model.state_dict(),
"input_size": input_size,
"hidden_size": hidden_size,
"output_size": output_size,
"all_words": all_words,
"tags": tags
}

FILE = "machine_learning/data.pth"
torch.save(data, FILE)

print(f'training complete. file saved to {FILE}')
