__author__ = 'Hannes Berntsson'

from keras.models import Sequential
from keras import layers
from keras.preprocessing.text import one_hot
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from keras.layers import Input, Embedding, LSTM, Bidirectional, Dense, Dropout, concatenate, Layer, GlobalMaxPooling1D, \
    BatchNormalization
from keras import Model
from sklearn.metrics import f1_score, recall_score, precision_score, confusion_matrix
import matplotlib.pyplot as plt


def build_model(feature_shape, target_shape):  # add embeddings and attention layer?
    model = Sequential()
    model.add(layers.Dense(100, input_dim=feature_shape, activation='relu'))
    model.add(layers.Dense(100, activation='softmax'))
    model.add(layers.Dense(target_shape, activation='sigmoid'))

    model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['categorical_accuracy'])
    model.summary()
    return model


def build_model_func(vocab_size, embedding_dim, embedding_weights):
    inp = Input(shape=(None,))
    entity_tags = Input(shape=(None, 2))  # 0 = No_entity, 1 = Entity1, 2= Entity 2

    x = Embedding(input_dim=vocab_size, output_dim=embedding_dim, weights=[embedding_weights], trainable=True)(
        inp)  # maskZero = True
    x = concatenate([x, entity_tags])
    # x = concatenate([x, trigram_input])
    x = Bidirectional(LSTM(200, recurrent_dropout=0.2, dropout=0.2))(x)
    x = Dense(64, activation="relu")(x)
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)
    x = Dense(3, activation="softmax")(x)

    model = Model([inp, entity_tags], x)
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=['categorical_accuracy'])
    model.summary()

    return model


def make_vectorizer(sentences, n_gram):
    if n_gram:
        vectorizer = CountVectorizer(analyzer="word", binary=True, ngram_range=(2, 3), lowercase=False,
                                     max_features=10000)
    else:
        vectorizer = CountVectorizer(min_df=0, lowercase=False)
    vectorizer.fit(sentences)
    return vectorizer


def train(model, X, y, epochs, X_test, y_test, batch_size, verbose):
    hist = model.fit(X, y, epochs=epochs, verbose=verbose, validation_data=(X_test, y_test), batch_size=batch_size)
    return hist


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


def pred_nonseq(model, x):
    return model.predict(x)


def create_embedding_matrix(vectors_path, words_path, word_index, embedding_dim):
    vocab_size = len(word_index) + 1  # Adding again 1 because of reserved 0 index
    embedding_matrix = np.zeros((vocab_size, embedding_dim))

    v = open(vectors_path)
    w = open(words_path, encoding="utf8")
    while True:
        word = w.readline()
        vector = v.readline().split()

        if word in word_index:
            i = word_index[word]
            embedding_matrix[i] = np.array(vector, dtype=np.float32)[:embedding_dim]

        if not word:
            break
    v.close()
    w.close()

    return embedding_matrix


def translate_results(results):
    predictions = []
    for result in results:
        predictions.append(result.tolist().index(1))
    return predictions


def translate_results_continuous(results):
    predictions = []
    for result in results:
        predictions.append(result.tolist().index(max(result.tolist())))
    return predictions


def print_fscores(true, predicted, average, labels):
    f_score = f1_score(y_true=true, y_pred=predicted, average=average, labels=labels)
    recall = recall_score(y_true=true, y_pred=predicted, average=average, labels=labels)
    precision = precision_score(y_true=true, y_pred=predicted, average=average, labels=labels)

    print("Recall: " + str(recall))
    print("Precision: " + str(precision))
    print("F-Score: " + str(f_score))

    return recall, precision, f_score


def print_confusion(true, predicted, labels):
    conf = confusion_matrix(true, predicted, labels=labels)
    print("Confusion Matrix:")
    print(conf)
    return conf


def count_predictions(predictions, string1, string2, string3):
    count0 = 0
    count1 = 0
    count2 = 0

    for pre in predictions:
        if pre == 0:
            count0 += 1
        if pre == 1:
            count1 += 1
        elif pre == 2:
            count2 += 1

    print(string1 + ": " + str(count0))
    print(string2 + ": " + str(count1))
    print(string3 + ": " + str(count2))


def plot_history(history):
    # Plot training & validation accuracy values
    plt.plot(history.history['categorical_accuracy'])
    plt.plot(history.history['val_categorical_accuracy'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()

    # Plot training & validation loss values
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()
