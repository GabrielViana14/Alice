import nltk
from nltk.stem import RSLPStemmer

stemmer = RSLPStemmer()
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('rslp')

def tokenize(sentence):
    return nltk.word_tokenize(sentence,language='portuguese')

def stem(word):
    return stemmer.stem(word)

def bag_of_words(tokenize_sentece, all_words):
    pass


if __name__ == "__main__":
    frase = "Olá esse é um exemplo de teste"
    frase_tokenizada = tokenize(frase)
    stemmed_words = [stem(w) for w in frase_tokenizada]
    print(frase_tokenizada)
    print(stemmed_words)
