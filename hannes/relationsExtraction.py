from bioInferTrainingParser import parse_training_set
import text_tools as tt
import copy
from RelationExtractorModel import RelationExtractorModel as REM
import random
import spacy


def main():
    inpts = parse_training_set('trainingFiles/BioInfer_corpus_1.2.0b.binarised.xml')

    # build the features
    features = []
    targets = []
    for inpt in inpts:
        #  print(inpt)
        interaction_list = inpt["interactions"]

        #  building features with interaction
        i = 0
        for interaction in interaction_list:
            try:
                ft = build_features(inpt, inpt["entities"][interaction[0]], inpt["entities"][interaction[1]])
            except ValueError:
                continue
            features.append(ft)
            targets.append(inpt['predicates'][i][2])
            i += 1

        entity_list = inpt["entities"]
        clean_entity_list = [x for x in entity_list if x is not None]
        if len(clean_entity_list) > 1:
            index1 = random.randint(0, len(clean_entity_list)-1)
            entity = clean_entity_list[index1]
            number = list(range(0, index1)) + list(range(index1+1, len(clean_entity_list)))
            entity2 = clean_entity_list[random.choice(number)]
            if not (entity is None or entity2 is None or entity == entity2 or [entity_list.index(entity), entity_list.index(entity)] in interaction_list):
                try:
                    ft2 = build_features(inpt, entity, entity2)
                    features.append(ft2)
                    targets.append('no_interaction')
                except ValueError:
                    pass

    rem = REM()

    sk = rem.split_data(features, targets, 0.75)
    train_feat = sk[0]
    train_targ = sk[2]
    test_feat = sk[1]
    test_targ = sk[3]
    print(train_feat[0])
    print(train_targ)
    rem.train(train_feat, train_targ)
    print(rem.predict(test_feat[0]))
    print("f1 = " + str(100*rem.sklearn_test(test_feat, test_targ)) + '%')


def build_features(inpt, entity, entity2):
    tokens = copy.copy(inpt["tokens"])

    if entity[0] < entity2[0]:
        tokens = join_tokens(tokens, entity, "ENTITY1")
        tokens = join_tokens(tokens, entity2, "ENTITY2")
    else:
        tokens = join_tokens(tokens, entity, "ENTITY2")
        tokens = join_tokens(tokens, entity2, "ENTITY1")

    sentence = " ".join(tokens)
    # pos = pos_tag(sentence)
    # print(pos)
    tokens = tt.tokenize(sentence)

    index1 = tokens.index("entity1")
    index2 = tokens.index("entity2")

    pre1 = build_gram(2, -1, tokens, index1)
    suf1 = build_gram(5, 1, tokens, index1)
    pre2 = build_gram(5, -1, tokens, index2)
    suf2 = build_gram(2, 1, tokens, index2)

    features = {'prefix1-m1': pre1[0],
                'prefix2-m1': pre1[1],
                'suffix1-m1': suf1[0],
                'suffix2-m1': suf1[1],
                'suffix3-m1': suf1[2],
                'suffix4-m1': suf1[3],
                'suffix5-m1': suf1[4],

                'suffix1-m2': suf2[0],
                'suffix2-m2': suf2[1],
                'prefix1-m2': pre2[0],
                'prefix2-m2': pre2[1],
                'prefix3-m2': pre2[2],
                'prefix4-m2': pre2[3],
                'prefix5-m2': pre2[4],

                'distance': index2-index1
                }

    return features


def build_gram(size, direction, tokens, index):
    index
    gram = list()
    for i in range(size):
        ind = index + direction*(1 + i)

        if ind < 0 or ind >= len(tokens):
            if direction < 0:
                gram = ['NaN'] + gram
            else:
                gram.append('NaN')
        else:
            if direction < 0:
                gram = [tokens[ind]] + gram
            else:
                gram.append(tokens[ind])
    return gram


def join_tokens(tokens, entity, string):
    tokens[entity[0]:entity[len(entity) - 1] + 1] = [string]
    return tokens


def build_token(tokens, entity):
    return ''.join(tokens[entity[0]:entity[len(entity) - 1] + 1])


def pos_tag(text):
    # spacy.load("sciSpacy/en_core_sci_md-0.2.0")
    nlp = spacy.load("en")
    doc = nlp(text)
    return [i for i in doc]


if __name__ == "__main__":
    main()
