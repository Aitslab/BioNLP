__author__ = 'Hannes Berntsson'

from keras_model import neural_model
from svm_model import RelationExtractorModel as REM
import random
import numpy as np
import pickle
import os
import glob
from itertools import permutations

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # export TF_CPP_MIN_LOG_LEVEL=2
import tensorflow as tf


def main():
    tf.logging.set_verbosity(tf.logging.ERROR)

    path = '../../olof_vilhelm/rels'
    inpts = []
    for filename in glob.glob(os.path.join(path, '*.p')):
        package = pickle.load(open(filename, 'rb'))
        for r in package:
            inpts.append(package[r])

    print("Building features...")
    sentences, targets = build_sentences_and_targets(inpts)
    neg_sentences, neg_targets = build_negatives(round(0.90 * len(sentences)), inpts)
    sentences = sentences + neg_sentences
    targets = targets + neg_targets

    no = 0
    pos = 0
    neg = 0
    for t in targets:
        if t == 'no_interaction':
            no += 1
        elif t == 'P':
            pos += 1
        else:
            neg += 1
    print('no_interaction:' + str(no))
    print('positive:' + str(pos))
    print('negative:' + str(neg))

    r_tot = 0
    p_tot = 0
    f_tot = 0
    conf_tot = np.zeros((3, 3))
    n = 10

    for i in range(n):
        X, X_test, y, y_test = REM.split_data(sentences, targets, 0.15)

        vec = neural_model.make_vectorizer(sentences, n_gram=True)
        X = vec.transform(X)
        X_test = vec.transform(X_test)

        y = transform_results(y, "no_interaction", "P", "N")
        y_test = transform_results(y_test, "no_interaction", "P", "N")

        model = neural_model.build_model(X.shape[1], y.shape[1])
        print("Training Model...")
        history = neural_model.train(model, X, y, 1, X_test, y_test, 500, verbose=False)

        print("Training set: ")
        neural_model.print_accuracy(model, X, y)
        print('\n')
        print("Test set: ")
        predicted = neural_model.pred(model, X_test)
        true = neural_model.translate_results(y_test)
        recall, precision, f_score = neural_model.print_fscores(true, predicted, 'weighted', [0, 1, 2])
        conf = neural_model.print_confusion(true, predicted, [0, 1, 2])
        neural_model.print_accuracy(model, X_test, y_test)

        conf_tot += conf
        r_tot += recall
        p_tot += precision
        f_tot += f_score

    print('')
    print('Average Recall: ' + str(r_tot / n))
    print('Average Precision: ' + str(p_tot / n))
    print('Average F-Score: ' + str(f_tot / n))
    print('Average Confusion Matrix: ' + '\n' + str(conf_tot / n))

    neural_model.plot_history(history)

    print("Building features...")
    vec = neural_model.make_vectorizer(sentences, n_gram=True)
    X = vec.transform(sentences)
    y = transform_results(targets, "no_interaction", "P", "N")
    model = neural_model.build_model(X.shape[1], y.shape[1])
    print("Training Model...")
    model.fit(X, y, epochs=25, verbose=True, batch_size=20)

    # pubmed = build_all_sentences(inpts, maxsize)
    # pickle.dump(pubmed, open("pubmed1.p", "wb"))
    pubmed = pickle.load(open('pubmed1.p', 'rb'))

    print(len(pubmed))
    X = vec.transform(pubmed)

    predictions = neural_model.pred(model, X)
    neural_model.count_predictions(predictions, "no_interaction", "P", "N")

    print(predictions)


def fix_sentence(inpt, interaction):
    entity1 = inpt["entities"][interaction[0] - 1]
    entity2 = inpt["entities"][interaction[1] - 1]

    tokens = inpt['tokens']

    if entity1[0] < entity2[0]:
        tokens = join_tokens(tokens, entity2, "ENTITY2")
        tokens = join_tokens(tokens, entity1, "ENTITY1")
    else:
        tokens = join_tokens(tokens, entity1, "ENTITY1")
        tokens = join_tokens(tokens, entity2, "ENTITY2")

    sentence = " ".join(tokens)
    return sentence


def join_tokens(tokens, entity, string):
    tokens[entity[0]:entity[len(entity) - 1] + 1] = [string]
    return tokens


def build_sentences_and_targets(inpts):
    sentences = []
    targets = []
    gen = (x for x in inpts if len(x['relations']) > 0)
    for inpt in gen:
        interaction_list = inpt["relations"]
        for interaction in interaction_list:
            try:
                sentences.append(fix_sentence(inpt, [interaction[0], interaction[1]]))
                targets.append(interaction[2])
            except ValueError:
                pass
    return sentences, targets


def build_all_sentences(inpts, maxsize):
    sentences = []
    i = 0
    for inpt in inpts:
        entities = inpt['entities']
        for pair in permutations(entities, r=2):
            sentences.append(fix_sentence(inpt, [entities.index(pair[0]), entities.index(pair[1])]))
            i += 1
        if i > maxsize:
            break
    return sentences


def build_negatives(nbr, inpts):
    features = []
    targets = []

    while len(features) < nbr:
        inpt = random.choice(inpts)
        entities = inpt['entities']
        if len(inpt['relations']) < 1:
            continue
        picked_entities = random.sample(entities, 2)
        interaction = [entities.index(picked_entities[0]), entities.index(picked_entities[1])]
        if not ([interaction[0], interaction[1]] in [[x, y] for x, y, z in inpt['relations']]):
            try:
                features.append(fix_sentence(inpt, interaction))
                targets.append('no_interaction')
            except ValueError:
                continue

    return features, targets


def clean_list(list):
    return [x for x in list if x is not None]


def entity_dist(sentence):
    return sentence.index("ENTITY2") - sentence.index("ENTITY1")


def transform_results(results, result1, result2, result3):
    array = []
    for result in results:
        if result == result1:
            row = [1, 0, 0]
        elif result == result2:
            row = [0, 1, 0]
        else:
            row = [0, 0, 1]
        array.append(row)

    return np.array(array)


if __name__ == "__main__":
    main()
