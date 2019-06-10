from bioInferTrainingParser import parse_training_set
import text_tools as tt
import copy
from RelationExtractorModel import RelationExtractorModel as REM
import random
import spacy


def main():
    inpts = parse_training_set('trainingFiles/BioInfer_corpus_1.2.0b.binarised.xml')
    nlp = spacy.load("en_core_sci_md")

    # build the features
    features = []
    targets = []
    print("Building features...")
    for inpt in inpts:
        #  building features with interaction

        entity_list = inpt["entities"]
        clean_entity_list = [x for x in entity_list if x is not None]
        interaction_list = inpt["interactions"]

        used = list()
        i = 0
        for interaction in interaction_list:
            try:
                ft = build_features(inpt, inpt["entities"][interaction[0]], inpt["entities"][interaction[1]], nlp)

                features.append(ft)
                targets.append(inpt['predicates'][i][0])  # inpt['predicates'][i][j] j = -> POS/NEG, etc.
                i += 1
            except ValueError:
                i += 1
                continue

            index1 = random.randint(0, len(clean_entity_list) - 1)
            entity = clean_entity_list[index1]
            number = list(range(0, index1)) + list(range(index1 + 1, len(clean_entity_list)))
            entity2 = clean_entity_list[random.choice(number)]

            if not ([entity_list.index(entity), entity_list.index(entity2)] in interaction_list or [entity_list.index(entity), entity_list.index(entity2)] in used):
                try:
                    ft2 = build_features(inpt, entity, entity2, nlp)
                except ValueError:
                    continue
                features.append(ft2)
                targets.append('no_interaction')
                used.append([entity_list.index(entity), entity_list.index(entity2)])

    print("Features Built!")

    r = 10
    sum_score = 0
    for i in range(r):
        rem = REM()

        train_feat, test_feat, train_targ, test_targ = rem.split_data(features, targets, 0.15)
        print(len(train_feat))
        print(test_targ)
        rem.train(train_feat, train_targ)
        pred = rem.model.decision_function(test_feat)
        print(pred)
        print(test_targ)

        fscore = 100*rem.sklearn_test(test_feat, test_targ, pred)
        print("f1 = " + str(fscore) + '%')
        sum_score += fscore
    print('Average f-score = ' + str(sum_score/r) + '%')


def build_features(inpt, entity, entity2, nlp):
    bad_tokens = copy.deepcopy(inpt['tokens'])

    if entity[0] < entity2[0]:
        tokens = join_tokens(bad_tokens, entity, "entity1")
        tokens = join_tokens(tokens, entity2, "entity2")
    else:
        tokens = join_tokens(bad_tokens, entity2, "entity1")
        tokens = join_tokens(tokens, entity, "entity2")

    sentence = " ".join(tt.tokenize(" ".join(tokens)))
    doc = nlp(sentence)

    tokens = list()
    pos = list()
    tag = list()
    dep = list()
    for token in doc:
        tokens.append(token.text)
        pos.append(token.pos_)
        tag.append(token.tag_)
        dep.append(token.dep_)

    index1 = tokens.index("entity1")
    index2 = tokens.index("entity2")

    window_size1 = 1
    window_size2 = 3

    pre1 = build_gram(window_size1, -1, tokens, index1)
    p_pos1 = build_gram(window_size1, -1, pos, index1)
    p_tag1 = build_gram(window_size1, -1, tag, index1)
    p_dep1 = build_gram(window_size1, -1, dep, index1)

    suf1 = build_gram(window_size2, 1, tokens, index1)
    s_pos1 = build_gram(window_size2, 1, pos, index1)
    s_tag1 = build_gram(window_size2, 1, tag, index1)
    s_dep1 = build_gram(window_size2, 1, dep, index1)

    pre2 = build_gram(window_size2, -1, tokens, index2)
    p_pos2 = build_gram(window_size2, -1, pos, index2)
    p_tag2 = build_gram(window_size2, -1, tag, index2)
    p_dep2 = build_gram(window_size2, -1, dep, index2)

    suf2 = build_gram(window_size1, 1, tokens, index2)
    s_pos2 = build_gram(window_size1, 1, pos, index2)
    s_tag2 = build_gram(window_size1, 1, tag, index2)
    s_dep2 = build_gram(window_size1, 1, dep, index2)

    features = {
                'prefix1-m1': pre1[0],

                'suffix1-m1': suf1[0],
                'suffix2-m1': suf1[1],
                'suffix3-m1': suf1[2],


                'p_pos1-m1': p_pos1[0],

                's_pos1-m1': s_pos1[0],
                's_pos2-m1': s_pos1[1],
                's_pos3-m1': s_pos1[2],


                'p_tag1-m1': p_tag1[0],

                's_tag1-m1': s_tag1[0],
                's_tag2-m1': s_tag1[1],
                's_tag3-m1': s_tag1[2],


                'p_dep1-m1': p_dep1[0],

                's_dep1-m1': s_dep1[0],
                's_dep2-m1': s_dep1[1],
                's_dep3-m1': s_dep1[2],


                'prefix1-m2': pre2[0],
                'prefix2-m2': pre2[1],
                'prefix3-m2': pre2[2],

                'suffix1-m2': suf2[0],


                'p_pos1-m2': p_pos2[0],
                'p_pos2-m2': p_pos2[1],
                'p_pos3-m2': p_pos2[2],

                's_pos1-m2': s_pos2[0],


                'p_tag1-m2': p_tag2[0],
                'p_tag2-m2': p_tag2[1],
                'p_tag3-m2': p_tag2[2],

                's_tag1-m2': s_tag2[0],


                'p_dep1-m2': p_dep2[0],
                'p_dep2-m2': p_dep2[1],
                'p_dep3-m2': p_dep2[2],

                's_dep1-m2': s_dep2[0],

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


def pos_tag(text, nlp):
    doc = nlp(text)
    return [i for i in doc]


if __name__ == "__main__":
    main()
