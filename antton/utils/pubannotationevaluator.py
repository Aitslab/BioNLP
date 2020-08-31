"""
PubAnnotation evaluator for COVID-19

Authors:
    Annie Tallind, Lund University, Faculty of Engineering
    Kaggle ID: atllnd
    Github ID: annietllnd

    Sofi Flink, Lund University, Faculty of Engineering
    Kaggle ID: sofiflinck
    Github ID: obakanue

    TODO:
     - Should we check correct word class?
"""
import os
import json
# true_positives = some_function() # number of true positives
# false_positives = some_other_function() # number of false positives
# true_negatives = other_function() # number of true negatives
# false_negatives = last_one() # number of false negatives
# for any is_checked = False in tagger_output_dict -> False positives
# for any is_checked = False in true_output_dict -> False negatives


def print_progress(nbr_pubannotations_evaluated, total_pubannotations):
    """
    Prints estimated progress based on number of total articles and number of articles processed.
    """
    print_progress_bar(nbr_pubannotations_evaluated,
                       total_pubannotations,
                       prefix='EVALUATION PROGRESS\t',
                       suffix='COMPLETE')


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Author: StackOverflow
            User Greenstick
            Question 30740258
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='', flush=True)
    # Print New Line on Complete
    if iteration == total:
        print()


class PubannotationEvaluator:
    """
    PubAnnotationEvaluator evaluates output compared to a true output, the arguments are the directory paths to the
    location of the outputs and a set containing what word classes/dictionaries to be evaluated.
    """
    def __init__(self, tagger_output_dir_path, true_output_dir_path, word_classes_set):
        self.tagger_output_dicts = dict()
        self.true_output_dicts = dict()
        self.word_classes_result_dict = dict()
        self.recall_values = list()
        self.precision_values = list()

        self.word_classes_set = word_classes_set
        self.true_positives = self.true_negatives = self.false_positives = self.false_negatives = \
            self.nbr_true_entities = self.recall_value = self.precision_value = self.total_true_positives = \
            self.total_false_positives = self.total_false_negatives = self.iteration_nbr = 0

        self.__generate_result_dict(self.word_classes_set)  # Initializes 'word_classes_result_dict'

        self.__load_output(tagger_output_dir_path, 1)  # Fill up the 'self.tagger_output_dicts' dict
        self.__load_output(true_output_dir_path, 0) # Fill up the 'self.true_output_dicts' dict

        self.processes_total = len(self.tagger_output_dicts) + len(self.word_classes_result_dict)

    def __generate_result_dict(self, word_classes_set):
        """
        Initializes a dictionary containing all the results for respective word class.
        """
        for word_class in word_classes_set:
            self.word_classes_result_dict[word_class] = {'total': {'amount': 0,
                                                                   'entities': list()
                                                                   },
                                                         'true_positives': {'amount': 0,
                                                                            'entities': list()
                                                                            },
                                                         'false_positives': {'amount': 0,
                                                                             'entities': list()
                                                                             },
                                                         'false_negatives': {'amount': 0,
                                                                             'entities': list()
                                                                             }
                                                         }
    def __load_output(self, dir_output_path, is_tagger_output):
        """
        Loads output files from a given directory in to corresponding dictionary. Second argument indicates if it is
        the true output or the output to be evaluated.
        """
        output_paths = os.listdir(dir_output_path)
        for pubannotation_file_name in output_paths:
            if pubannotation_file_name == '.DS_Store':  # For MacOS users skip .DS_Store-file
                continue                                # generated.
            full_path = dir_output_path + pubannotation_file_name
            with open(full_path) as pubannotation_obj:
                pubannotation_dict = json.loads(pubannotation_obj.read())
                pubannotation_dict.update({'is_checked': False})
                if is_tagger_output:
                    self.tagger_output_dicts.update({pubannotation_file_name: pubannotation_dict})
                else:
                    self.true_output_dicts.update({pubannotation_file_name: pubannotation_dict})

    def evaluate(self):
        """
        Evaluates outputs compared to true outputs.
        """
        self.__compare_outputs()
        self.__evaluate_word_class()
        self.__calculate_micro()
        self.__print_result('MICRO')
        self.__calculate_macro()
        self.__print_result('MACRO')
        self.__calculate_harmonic_mean()

    def __compare_outputs(self):
        """
        Iterates through all outputs to be compared to through output and compare output denotations.
        """
        for cord_uid in self.tagger_output_dicts:  # 'cord_uid' is the file name!!
            print_progress(self.iteration_nbr, self.processes_total)
            tagger_pubannotation = self.tagger_output_dicts[cord_uid]  # Full file (predicted)
            if cord_uid in self.true_output_dicts: # 'cord_uid' is the file name!!
                true_pubannotation = self.true_output_dicts[cord_uid]  # Full file (true)
                text = true_pubannotation['text']
                word_classes_list = [denotations_list_element['obj'] for denotations_list_element in
                                     true_pubannotation['denotations']] # List of denotation IDs
                self.__compare_output(tagger_pubannotation,
                                      true_pubannotation,
                                      cord_uid,
                                      word_classes_list,
                                      text)
                self.iteration_nbr += 1
        print_progress(self.iteration_nbr, self.processes_total)

    def __compare_output(self, tagger_pubannotation, true_pubannotation, cord_uid, word_classes_list, text):
        """
        Compares denotations with true denotations, false negatives field are incremented if there is a an existing
        match in true denotations that does not exist in denotations to be compared, and only for the word classes
        existing in the list argument. When a denotation is checked the field 'is_checked' is set to True which
        helps to calculate false positives and false negatives. If two denotations are matching in span true positives
        filed will be incremented in the result dictionary.
        """
        tagger_denotations = tagger_pubannotation['denotations'] #Add key 'is_checked' to all denotations in both files
        for tagger_denotation in tagger_denotations:
            tagger_denotation['is_checked'] = False
        true_denotations = true_pubannotation['denotations']
        for true_denotation in true_denotations:
            true_denotation['is_checked'] = False

        #TRUE POSITIVES
        for tagger_denotation in tagger_denotations:
            i = 0
            for true_denotation in true_denotations:
                tagger_denotation_span = (tagger_denotation['span']['begin'], tagger_denotation['span']['end'])
                true_denotation_span = (true_denotation['span']['begin'], true_denotation['span']['end'])
                if tagger_denotation_span == true_denotation_span:
                    # Might want to change to a safer implementation where we don't depend on an ordered
                    # word_classes_list. TODO

                    if word_classes_list[i] in self.word_classes_set and tagger_denotation['obj'] == true_denotation['obj']:
                        word_class = word_classes_list[i]
                        self.word_classes_result_dict[word_class]['true_positives']['amount'] += 1
                        self.word_classes_result_dict[word_class]['total']['amount'] += 1
                        self.word_classes_result_dict[word_class]['true_positives']['entities'].append(
                            f'id: {word_class}, '
                            f'entity: {text[tagger_denotation_span[0]:tagger_denotation_span[1] + 1]}, '
                            f'span: {tagger_denotation_span}')
                        self.word_classes_result_dict[word_class]['total']['entities'].append(
                            f'id: {word_class}, '
                            f'entity: {text[tagger_denotation_span[0]:tagger_denotation_span[1] + 1]}, '
                            f'span: {tagger_denotation_span}')
                        true_denotation.update({'is_checked': True})
                        tagger_denotation.update({'is_checked': True})
                        break
                i += 1

        #FALSE POSITIVES
        for tagger_denotation in tagger_denotations:
            if not tagger_denotation['is_checked']:
                word_class = tagger_denotation['obj']
                if word_class in self.word_classes_set:  # If 'obj' is in the allowed terms
                    tagger_denotation_span = (tagger_denotation['span']['begin'], tagger_denotation['span']['end'])
                    self.word_classes_result_dict[word_class]['false_positives']['amount'] += 1
                    self.word_classes_result_dict[word_class]['false_positives']['entities'].append(
                        f'id: {word_class}, '
                        f'entity: {text[tagger_denotation_span[0]:tagger_denotation_span[1] + 1]}, '
                        f'span: {tagger_denotation_span}')
                tagger_denotation.update({'is_checked': True})

        #FALSE NEGATIVES
        for true_denotation in true_denotations:
            word_class = true_denotation['obj']
            if word_class in self.word_classes_set:
                if not true_denotation['is_checked']:
                    true_denotation_span = (true_denotation['span']['begin'], true_denotation['span']['end'])
                    self.word_classes_result_dict[word_class]['false_negatives']['amount'] += 1
                    self.word_classes_result_dict[word_class]['total']['amount'] += 1
                    self.word_classes_result_dict[word_class]['false_negatives']['entities'].append(
                        f'id: {word_class}, '
                        f'entity: {text[true_denotation_span[0]:true_denotation_span[1] + 1]}, '
                        f'span: {true_denotation_span}')
                true_denotation.update({'is_checked': True})



    def __evaluate_word_class(self):
        """
        Evaluates results for each word class.
        """
        for word_class in self.word_classes_result_dict:
            print_progress(self.iteration_nbr, self.processes_total)
            self.__precision(word_class)
            self.__recall(word_class)
            self.__print_result(word_class)
            self.iteration_nbr += 1
        print_progress(self.iteration_nbr, self.processes_total)

    def __precision(self, word_class):
        """
        Calculates precision figure.
        """
        true_positives = self.word_classes_result_dict[word_class]['true_positives']['amount']
        false_positives = self.word_classes_result_dict[word_class]['false_positives']['amount']
        self.total_true_positives += true_positives
        self.total_false_positives += false_positives
        sum_value = true_positives + false_positives
        if sum_value:
            self.precision_value = true_positives / sum_value
            self.precision_values.append(self.precision_value)
        else:
            print("\n")
            print('########### WARNING ###########')
            print(f'{word_class} found no match, the precision result can be misleading')
            print("########### WARNING ###########")
            self.precision_value = 0

    def __recall(self, word_class):
        """
        Calculates recall figure.
        """
        true_positives = self.word_classes_result_dict[word_class]['true_positives']['amount']
        false_negatives = self.word_classes_result_dict[word_class]['false_negatives']['amount']
        self.total_false_negatives += false_negatives
        sum_value = true_positives + false_negatives
        if sum_value:
            self.recall_value = true_positives / sum_value
            self.recall_values.append(self.recall_value)
        else:
            print('########### WARNING ###########')
            print(f"'{word_class}' found no match, the recall result can be misleading")
            print('########### WARNING ###########')
            print('\n')
            self.precision_values.append(0)
            self.recall_value = 0

    def __calculate_micro(self):
        """
        Calculates micro figure.
        """
        sum_value = self.total_true_positives + self.total_false_positives
        if sum_value:
            self.precision_value = self.total_true_positives / (self.total_true_positives + self.total_false_positives)
            self.recall_value = self.total_true_positives / (self.total_true_positives + self.total_false_negatives)
        else:
            self.precision_value = 0
            self.recall_value = 0

    def __calculate_macro(self):
        """
        Calculates macro figure.
        """
        self.precision_value = 0
        self.recall_value = 0
        for precision_value in self.precision_values:
            self.precision_value += precision_value
        for recall_value in self.recall_values:
            self.recall_value += recall_value
        if self.precision_value:
            self.precision_value /= len(self.precision_values)
            self.recall_value /= len(self.recall_values)

    def __calculate_harmonic_mean(self):
        """
        Calculates harmonic mean/F1 score figure.
        """
        sum_value = self.precision_value + self.recall_value
        harmonic_mean = 0
        if sum_value:
            harmonic_mean = (2*self.precision_value*self.recall_value) / sum_value
        print(f'#########\tHARMONIC MEAN RESULT:\t###########')
        print(f'Harmonic mean:\t{harmonic_mean * 100:.0f}%')

    def __print_result(self, word_class):
        """
        Prints result for a given section/word class.
        """
        print(f'\n\n#########\t{word_class.upper()} PRECISION & RECALL RESULT:\t###########')
        print('\n')
        print(f'Precision:\t{self.precision_value * 100:.0f}%')
        print(f'Recall:\t\t{self.recall_value * 100:.0f}%')
        print('\n')

    def get_total_entities(self, word_class):
        """
        Returns a list of total entities for a word class.
        """
        return self.word_classes_result_dict[word_class]['total']['entities']

    def get_true_positive_entities(self, word_class):
        """
        Returns a list of entities marked as true positives for a word class.
        """
        return self.word_classes_result_dict[word_class]['true_positives']['entities']

    def get_false_positive_entities(self, word_class):
        """
        Returns a list of entities marked as false positives for a word class.
        """
        return self.word_classes_result_dict[word_class]['false_positives']['entities']

    def get_false_negative_entities(self, word_class):
        """
        Returns a list of entities marked as false negatives for a word class.
        """
        return self.word_classes_result_dict[word_class]['false_negatives']['entities']

    def get_total(self, word_class):
        """
        Returns number of entities associated with a word class.
        """
        return self.word_classes_result_dict[word_class]['total']['amount']

    def get_true_positives(self, word_class):
        """
        Returns number of true positives associated with a word class.
        """
        return self.word_classes_result_dict[word_class]['true_positives']['amount']

    def get_false_positives(self, word_class):
        """
        Returns number of false positives associated with a word class.
        """
        return self.word_classes_result_dict[word_class]['false_positives']['amount']

    def get_false_negatives(self, word_class):
        """
        Returns number of false negatives associated with a word class.
        """
        return self.word_classes_result_dict[word_class]['false_negatives']['amount']
