from bioInferTrainingParser import parse_training_set
import text_tools as tt


def main():
    inpts = parse_training_set('trainingFiles/BioInfer_corpus_1.2.0b.binarised.xml')
    test_text = inpts[0]['text']
    print(tt.tokenize(test_text))

    # build the features
    features = list()
    target = list()
    #  for inpt in inpts:


if __name__ == "__main__":
    main()
