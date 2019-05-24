__author__ = 'Hannes Berntsson'

from keras.models import Sequential
from keras import layers
from keras.preprocessing.text import one_hot
from sklearn.feature_extraction.text import CountVectorizer
from keras.optimizers import Adam


def build_model(feature_shape, target_shape):  # add embeddings and attention layer?
    model = Sequential()
    model.add(layers.Dense(100, input_dim=feature_shape, activation='relu'))
    model.add(layers.Dense(100, activation='softmax'))
    model.add(layers.Dense(target_shape, activation='sigmoid'))

    opt = Adam(lr=.0001)
    model.compile(loss='mean_squared_error', optimizer='Adam', metrics=['accuracy'])
    model.summary()
    return model


def make_vectorizer(sentences, n_gram):
    if n_gram:
        vectorizer = CountVectorizer(analyzer="word", binary=True, ngram_range=(3, 3), lowercase=False)
    else:
        vectorizer = CountVectorizer(min_df=0, lowercase=False)
    vectorizer.fit(sentences)
    return vectorizer


def train(model, X, y, epochs, X_test, y_test, batch_size, verbose):
    model.fit(X, y, epochs=epochs, verbose=verbose, validation_data=(X_test, y_test), batch_size=batch_size)


def print_accuracy(model, X, y):
    loss, accuracy = model.evaluate(X, y, verbose=False)
    print("Accuracy: {:.4f}".format(accuracy))
    print("Loss: {:.4f}".format(loss))
    return loss, accuracy


def one_hot_list(text_list):
    list_one_hot = [one_hot(text, n=200000, lower=False) for text in text_list]
    return list_one_hot


def one_hott(text):
    return one_hot(text, n=200000)


def pred(model, x):
    return model.predict_classes(x)
