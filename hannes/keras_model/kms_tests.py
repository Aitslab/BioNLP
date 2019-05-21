from keras_model import kms
from bioInferTrainingParser import parse_training_set
from RelationExtractorModel import RelationExtractorModel as REM
from keras.preprocessing.text import Tokenizer
from keras.datasets import reuters
import spacy
import copy
import random
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # export TF_CPP_MIN_LOG_LEVEL=2
import tensorflow as tf
import keras


def main():
    if tf.test.gpu_device_name():
        print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
    else:
        print("Please install GPU version of TF")
        
    inpts = parse_training_set('../trainingFiles/BioInfer_corpus_1.2.0b.binarised.xml')
    nlp = spacy.load("en_core_sci_md")

    print("Building features...")
    training_sentences, training_targets = build_sentences_and_targets(inpts, nlp)
    X_neg, y_neg = build_negatives(round(2*len(training_sentences)), inpts, nlp)
    training_sentences = training_sentences + X_neg
    training_targets = training_targets + y_neg
    print("Features: " + str(training_sentences))
    print("Targets: " + str(training_targets))

    training_sentences, test_sentences, training_targets, test_targets = REM.split_data(training_sentences, training_targets, 0.2)

    # (x_trainn, y_trainn), (x_testt, y_testt) = reuters.load_data(test_split=0.2)
    #
    # print(x_trainn)
    # print(y_trainn)
    #
    # tokenizer = Tokenizer(num_words=200000)
    # X = tokenizer.sequences_to_matrix(X, mode='binary')
    # X_test = tokenizer.sequences_to_matrix(X_test, mode='binary')

    print(len(training_sentences))
    print(len(test_sentences))
    print(training_sentences)
    print(training_targets)

    vec = kms.make_vectorizer(training_sentences)
    print(vec.vocabulary_)
    X = vec.transform(training_sentences)
    X_test = vec.transform(test_sentences)

    vecy = kms.make_vectorizer(training_targets)
    print(vecy.vocabulary_)
    y = vecy.transform(training_targets)
    y_test = vecy.transform(test_targets)

    # print(X)
    # print(X[0])
    print(X.shape[1])
    print(y)

    print('\n')
    model = kms.build_model(X.shape[1], y.shape[1])
    print("Training Model...")
    kms.train(model, X, y, 30, X_test, y_test, 20)
    print("Training set: ")
    kms.print_accuracy(model, X, y)
    print('\n')
    print("Test set: ")
    kms.print_accuracy(model, X_test, y_test)

    # print_me = ""
    # for i in range(100):
    #     print_me += str(kms.pred(model, X_test[i])) + ", " + str(test_targets[i])
    # print(print_me)


def fix_sentence(inpt, interaction, nlp):
    entity1 = inpt["entities"][interaction[0]]
    entity2 = inpt["entities"][interaction[1]]

    tokens = copy.deepcopy(inpt['tokens'])

    if entity1[0] < entity2[0]:
        tokens = join_tokens(tokens, entity2, "ENTITY2")
        tokens = join_tokens(tokens, entity1, "ENTITY1")
    else:
        tokens = join_tokens(tokens, entity1, "ENTITY1")
        tokens = join_tokens(tokens, entity2, "ENTITY2")

    # doc = nlp(" ".join(tokens))
    sentence = " ".join(tokens)
    # print(sentence)
    return sentence


def join_tokens(tokens, entity, string):
    tokens[entity[0]:entity[len(entity) - 1] + 1] = [string]
    return tokens


def build_sentences_and_targets(inpts, nlp):
    sentences = []
    targets = []
    for inpt in inpts:

        interaction_list = inpt["interactions"]
        i = 0
        for interaction in interaction_list:
            try:
                sentences.append(fix_sentence(inpt, interaction, nlp))
                targets.append(inpt['predicates'][i][0])  # inpt['predicates'][i][j] j = -> POS/NEG, etc.
            except ValueError:
                pass
            i += 1
    return sentences, targets


def build_negatives(nbr, inpts, nlp):
    features = []
    targets = []

    while len(features) < nbr:
        inpt = random.choice(inpts)
        entities = inpt['entities']
        clean_entity_list = clean_list(inpt['entities'])
        if len(clean_entity_list) < 2:
            continue
        picked_entities = random.sample(clean_entity_list, 2)
        interaction = [entities.index(picked_entities[0]), entities.index(picked_entities[1])]
        if not ([interaction[0], interaction[1]] in inpt['interactions']):
            try:
                features.append(fix_sentence(inpt, interaction, nlp))
                targets.append('no_interaction')
            except ValueError:
                continue

    return features, targets


def clean_list(list):
    return [x for x in list if x is not None]


def entity_dist(sentence):
    return sentence.index("ENTITY2") - sentence.index("ENTITY1")


if __name__ == "__main__":
    main()
