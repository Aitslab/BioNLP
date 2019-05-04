import xml.etree.cElementTree as xmlET
import os


def parse_training_set(file_name):
    tree = xmlET.parse(file_name)
    root = tree.getroot()

    inputs = list()
    #  print(root.tag, root.attrib)
    for sentence_list in root.findall('Sentences'):
        #  print(sentence_list.tag, sentence_list.attrib)

        for sentence in sentence_list.findall('Sentence'):
            entry = dict()
            entry['text'] = sentence.find('SentenceText').text
            entry['drug'] = sentence.find('Sentence').get('LabelDrug')
            #  print(sentence.tag, sentence.attrib)
            #  print(text.text)

            mentions = list()
            for mention in sentence.findall('Mention'):
                mention_dict = dict()
                #  print(mention.tag, mention.attrib)
                mention_dict['id'] = mention.get('id')
                mention_dict['text'] = mention.get('str')
                mention_dict['type'] = mention.get('type')
                mention_dict['span'] = mention.get('span')
                mentions.append(mention_dict)
            entry['mentions'] = mentions

            interactions = list()
            for interaction in sentence.findall('Interaction'):
                interaction_dict = dict()
                #  print(interaction.tag, interaction.attrib)

                interaction_dict['type'] = interaction.get('type')
                interaction_dict['trigger'] = interaction.get('trigger')
                interaction_dict['precipitant'] = interaction.get('precipitant')
                effect = interaction.get('precipitant')
                #  print(type(effect))
                if effect is not None:
                    interaction_dict['effect'] = effect
                interactions.append(interaction_dict)
            entry['interactions'] = interactions
            inputs.append(entry)

    return inputs


def parse_all_files(directory):
    inputs = list()
    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            #  print(os.path.join(directory, filename))
            inputs += parse_training_set(os.path.join(directory, filename))
    return inputs


#  inp = parse_training_set("trainingFiles/ADCIRCA_ff61b237-be8e-461b-8114-78c52a8ad0ae.xml")
# inp = parse_all_files("trainingFiles/")
# print(inp[1])
# print(inp[len(inp) - 1])
# print(len(inp))
