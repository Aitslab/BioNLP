import nltk
import keras.preprocessing.text as kpt


def normalize(text):
    #  returns inputted string normalized (lower case)
    return text.lower()


def tokenize(text):
    #  returns text tokenized (normalized and stoppers removed) using keras functions
    #  return nltk.word_tokenize(text)
    return kpt.text_to_word_sequence(text)


def remove_stoppers(tokens):
    #  returns tokens with stopper words removed
    new_tokens = []
    for token in tokens:
        if token in nltk.corpus.stopwords.words('english'):
            continue
        new_tokens.append(token)
    return new_tokens


def clean_tokens(tokens):
    #  returns tokens without stopper words, digits and single letter words
    new_tokens = []
    for token in tokens:
        if token in nltk.corpus.stopwords.words('english') or token.isdigit() or len(token) < 2:
            continue
        new_tokens.append(token)
    return new_tokens


def replace_tokens(tokens, word_variations, new_word):
    #  returns tokens having replaced all instances of the set (or string) word_variations with new_word
    new_tokens = []
    for token in tokens:
        if token in word_variations:
            new_tokens.append(new_word)
        else:
            new_tokens.append(token)
    return new_tokens
