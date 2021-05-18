import random
import json

relations = ["NOT", "PART-OF", "INTERACTOR", "REGULATOR-POSITIVE", "REGULATOR-NEGATIVE"] 

cl_to_cid = {"NOT":                 "0",
            "PART-OF":              "1",
            "INTERACTOR":           "2",
            "REGULATOR-POSITIVE":   "3",
            "REGULATOR-NEGATIVE":   "4",
            }
              
for relation in relations:
  part1_list = []
  part2_list = []
  part3_list = []
  part4_list = []
  part5_list = []

  with open("element1.txt", "r") as file:
    for line in file:
      part1_list.append(line.replace('\n',''))

  with open("element1_mixed.txt", "r") as file:
    for line in file:
      part1_list.append(line.replace('\n',''))

  part1_list.append('')

  with open("element2_4_protein_names_uniprot.txt", "r") as file: #switch input file for a different type of entity
    for line in file:
      part2_list.append(line.replace('\n',''))

  with open("element3_{}.txt".format(relation), "r") as file: #switch input file for a different type of relation
    for line in file:
      part3_list.append(line.replace('\n',''))

  with open("element2_4_protein_names_uniprot.txt", "r") as file: #switch input file for a different type of entity
    for line in file:
      part4_list.append(line.replace('\n',''))

  with open("element5_disease.txt", "r") as file:
    for line in file:
      part5_list.append(line.replace('\n',''))

  with open("element5_process.txt", "r") as file:
    for line in file:
      part5_list.append(line.replace('\n',''))

  with open("element5_mixed.txt", "r") as file:
    for line in file:
      part5_list.append(line.replace('\n',''))

  part5_list.append('')

  sentences = []
    
  for i in range(10000): #select number of sentences that should be produced
    part1   = random.choice(part1_list)
    part2   = random.choice(part2_list)
    part3   = random.choice(part3_list)
    part4   = random.choice(part4_list)
    part5   = random.choice(part5_list)
    string  = part1+' << '+part2+' >> '+part3+'[[ '+part4+' ]] '+part5
    sentences.append(string.replace('  ',' ').strip())

  with open('corpus_P-{}-P_1-2.txt'.format(relation),'w', encoding = 'utf-8') as outfile: 

  # compose file name as follows:
  # entity type (P = protein, C = chemical), 
  # interaction type
  # direction 1-2 (first entity does something to second entity) or 2-1
    for sentence in sentences:
        outfile.write(json.dumps(
          {"text": sentence,
           "custom_label": relation,
           "cid": cl_to_cid[relation]
        }))
        outfile.write('\n')


# merge corpus files into one training file
with open("artificial_train.txt", "w") as outfile:
    for relation in relations:
        with open("corpus_P-{}-P_1-2.txt".format(relation)) as infile:
            contents = infile.read()
            outfile.write(contents)
