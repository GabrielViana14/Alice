import nltk
from nltk.stem import RSLPStemmer
import numpy as np

# Inicializando o stemmer e baixando os recursos necessários
stemmer = RSLPStemmer()
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('rslp')
language = 'portuguese'

class NltkUtils():
    def tokenize(self, sentence):
        """
        Separa a frase em uma array de palavras/tokens.
        Um token pode ser uma palavra, pontuação ou número.
        """
        return nltk.word_tokenize(sentence, language=language)

    def stem(self, word):
        """
        Stemização(Derivação) = É o processo de reduzir palavras flexionadas ao seu tronco, base ou raiz,
        geralmente uma forma da palavra escrita.
        Exemplo:
        words = ["amigos", "amigas", "amizade", "carreira", "carreiras"]
        words = [stem(w) for w in words]
        -> ["amig", "amig", "amizad", "carr", "carr"]
        """
        return stemmer.stem(word.lower())

    def bag_of_words(self, tokenize_sentence, all_words):
        """
        Retorna uma array de pacote de palavras:
        1 para cada palavra encontrada na frase, 0 caso não encontre
        Exemplo:
        sentence = ["hello", "how", "are", "you"]
        words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
        bag   = [  0 ,    1 ,    0 ,   1 ,    0 ,    0 ,      0]
        """
        # Deriva cada palavra
        sentence_words = [self.stem(word) for word in tokenize_sentence]

        # Inicia a bag com 0 para cada palavra
        bag = np.zeros(len(all_words), dtype=np.float32)

        for idx, w in enumerate(all_words):
            if w in sentence_words:
                bag[idx] = 1

        return bag

if __name__ == "__main__":
    nltk_utils = nltk_utils()

    frase = "Olá esse é um exemplo de teste"
    frase_tokenizada = nltk_utils.tokenize(frase)
    stemmed_words = [nltk_utils.stem(w) for w in frase_tokenizada]
    
    print("Frase tokenizada:", frase_tokenizada)
    print("Palavras derivadas:", stemmed_words)
    
    # Exemplo de uso da função bag_of_words
    all_words = ["olá", "esse", "é", "um", "exemplo", "de", "teste", "outro"]
    bag = nltk_utils.bag_of_words(frase_tokenizada, all_words)
    print("Bag of words:", bag)
