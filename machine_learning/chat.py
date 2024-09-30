import random
import json
import torch
from machine_learning.model.NeuralNet import NeuralNet
from machine_learning.nltk_utils import NltkUtils

nltkutils = NltkUtils()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('machine_learning/intents/ptbr/intents.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)

FILE = "machine_learning/data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

class Chat():
    def __init__(self):
        pass

    def resposta(self,entrada):
        sentence = nltkutils.tokenize(entrada)
        X = nltkutils.bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        output = model(X)
        _, predicted = torch.max(output, dim=1)
        tag = tags[predicted.item()]
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > 0.75:
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    return random.choice(intent['responses'])
        else:
            return "Eu não entendi..."


if __name__ == "__main__":
    answer = Chat()
    pergunta = ""
    while pergunta.lower() != "sair":
        pergunta = input("Entrada: ")
        print(answer.resposta(pergunta))
