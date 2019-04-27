from bioInferTrainingParser import parse_training_set
import text_tools as tt
import copy
from RelationExtractorModel import RelationExtractorModel as REM
import random


def main():
    inpts = parse_training_set('trainingFiles/BioInfer_corpus_1.2.0b.binarised.xml')
    test_text = inpts[0]['text']
    # print(tt.tokenize(test_text))

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
    tokens = tt.tokenize(sentence)

    index1 = tokens.index("entity1")
    index2 = tokens.index("entity2")

    left = list()
    right = list()

    for i in range(2):
        in1 = index1 - 1 - i
        in2 = index2 + 1 + i

        if in1 < 0:
            left = ['NaN'] + left
        else:
            left = [tokens[in1]] + left
        if in2 > len(tokens) - 1:
            right.append('NaN')
        else:
            right.append(tokens[in2])

    for i in range(5):
        in1 = index1 + 1 + i
        in2 = index2 - 1 - i

        if in1 > len(tokens) - 1:
            left.append('NaN')
        else:
            left.append(tokens[in1])
        if in2 < 0:
            right = ['NaN'] + right
        else:
            right = [tokens[in2]] + right

    features = {'prefix1-m1': left[0],
                'prefix2-m1': left[1],
                'suffix1-m1': left[2],
                'suffix2-m1': left[3],
                'suffix3-m1': left[4],
                'suffix4-m1': left[5],
                'suffix5-m1': left[6],

                'suffix1-m2': right[0],
                'suffix2-m2': right[1],
                'prefix1-m2': right[2],
                'prefix2-m2': right[3],
                'prefix3-m2': right[4],
                'prefix4-m2': right[5],
                'prefix5-m2': right[6],

                'distance': index2-index1
                }

    return features


def join_tokens(tokens, entity, string):
    tokens[entity[0]:entity[len(entity) - 1] + 1] = [string]
    return tokens


def build_token(tokens, entity):
    return ''.join(tokens[entity[0]:entity[len(entity) - 1] + 1])


if __name__ == "__main__":
    main()
