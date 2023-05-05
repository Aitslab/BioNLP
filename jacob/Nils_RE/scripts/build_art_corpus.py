import random
import json

relations = ["NOT", "PART-OF", "INTERACTOR", "REGULATOR-POSITIVE", "REGULATOR-NEGATIVE"]

cl_to_cid = {"NOT":                   "0",
              "PART-OF":              "1",
              "INTERACTOR":           "2",
              "REGULATOR-POSITIVE":   "3",
              "REGULATOR-NEGATIVE":   "4",
            }

def build_corpus(input_path, relation, class_size):          
    start_list = []
    protein_list = []
    chemical_list = []
    interaction_list = []
    end_list = []

    with open(input_path + "element1.txt", "r") as file:
      for line in file:
        start_list.append(line.replace('\n',''))

    with open(input_path + "element1_mixed.txt", "r") as file:
      for line in file:
        start_list.append(line.replace('\n',''))

    start_list.append('')

    with open(input_path + "element2_4_protein_names_uniprot.txt", "r") as file: #switch input file for a different type of entity
      for line in file:
        protein_list.append(line.replace('\n',''))

    with open(input_path + "element2_4_chemical_names_chemprot.txt", "r", encoding="utf8") as file: #switch input file for a different type of entity
      for line in file:
        chemical_list.append(line.replace('\n',''))

    with open(input_path + "element3_{}.txt".format(relation), "r") as file: #switch input file for a different type of relation
      for line in file:
        interaction_list.append(line.replace('\n',''))

    with open(input_path + "element5_disease.txt", "r") as file:
      for line in file:
        end_list.append(line.replace('\n',''))

    with open(input_path + "element5_process.txt", "r") as file:
      for line in file:
        end_list.append(line.replace('\n',''))

    with open(input_path + "element5_mixed.txt", "r") as file:
      for line in file:
        end_list.append(line.replace('\n',''))

    end_list.append('')

    sentences = []
      
    for i in range(class_size): #select number of sentences that should be produced
      start_phrase         = random.choice(start_list)
      interaction_phrase   = random.choice(interaction_list)
      end_phrase           = random.choice(end_list)
      chemical             = random.choice(chemical_list)
      protein              = random.choice(protein_list)
      
      entity_order = random.choice(["chem-prot", "prot-chem"])
      if entity_order == "chem-prot":
        string  = start_phrase +' << '+chemical+' >> '+interaction_phrase+'[[ '+protein+' ]] '+end_phrase
      elif entity_order == "prot-chem":
        string  = start_phrase +' << '+protein+' >> '+interaction_phrase+'[[ '+chemical+' ]] '+end_phrase

      sentences.append(string.replace('  ',' ').strip())

    with open('corpus_PC-{}-PC_1-2.txt'.format(relation),'w', encoding = 'utf-8') as outfile: 
    # with open('corpus_P-{}-P_1-2.txt'.format(relation),'w', encoding = 'utf-8') as outfile: 
      # compose file name as follows:
      # entity type (P = protein, C = chemical, PC = random mix), 
      # interaction type
      # direction 1-2 (first entity does something to second entity) or 2-1
      for sentence in sentences:
          outfile.write(json.dumps(
            {"text": sentence,
            "custom_label": relation,
            "cid": cl_to_cid[relation]
          }))
          outfile.write('\n')

def write_corpus(output_path):
  # merge corpus files into one training file
  with open(output_path, "w") as outfile:
      for relation in relations:
          with open("corpus_PC-{}-PC_1-2.txt".format(relation)) as infile:
              contents = infile.read()
              outfile.write(contents)

def run(input_path, output_path, class_size):
  for relation in relations:
    build_corpus(input_path, relation, class_size)
  
  write_corpus(output_path)
