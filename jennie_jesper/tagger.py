import sys, os, pathlib, json
from os import listdir
from os.path import isfile, join
import re
import time

dicts = {}

def path_to_paper_id(path):
     '''
     returns a paper_id given the input path of the file
     '''
     return path.split("/")[-1][:-5]

def read_article(path):
     '''
     returns a list with the title, abstract and body_text from given input path
     '''
     ret = []
     with open(path) as f:
          d = json.load(f)
          ret.append((d["metadata"]["title"], "title"))
          for t in d["abstract"]:
               ret.append((t["text"], "abstract"))
          for t in d["body_text"]:
               ret.append((t["text"], "body_text"))
     return ret

def read_meta(paperid, metaf):
     '''
     returns a list of [cord_uid, sourcedb, sourceid, obj]
     from input paperid and metafile. If not found returns [0,0,0,0]
     '''
     metafile = open(metaf, "r")
     for line in metafile:
          if paperid in line:
               metaline = line.split(",")
               cord_uid = metaline[0]
               sourcedb = metaline[2]
               sourceid = metaline[5]
               obj = metaline[-1]
               return [cord_uid, sourcedb, sourceid, obj]
     return [0,0,0,0]

def setup_dicts(dicts_folder_path):
     '''
     takes the folder path of the dictionaries (classes) as input and sets up the keys
     from the .txt file names of the classes. The keys and values are stored in the 
     variable dicts and each key will be mapped to a list of phrases sorted on length
     with longest first.
     '''
     dicts_paths = [dicts_folder_path + "/" + f  for f in os.listdir(dicts_folder_path)]

     for d in dicts_paths:
          cat = d.split("/")[-1][:-4]
          phrase_list = [line.strip() for line in open (d)]
          phrase_list.sort(key = len, reverse=True)
          dicts[cat] = phrase_list

def tag_article(article_path, metaf):
     '''
     takes input article_path and associated metafile and returns the denotated_sections
     for one complete article. Tagging is done section for section for the input article.
     Matches from two different dictionaries are allowed, but not from the same dictionary.
     Longer matches are prioritized.
     '''
     article = read_article(article_path)
     denotated_sections = []
     obj = read_meta(path_to_paper_id(article_path), metaf)[3]

     for section in article:
          section = section[0].lower()
          section = section.replace('-', ' ')
          denotations = []
          for cat in dicts.keys():
               #below are the most important lines in the program
               #re_or will for each cat (category) be a string built up by the sorted
               #content of the corresponding dictionary. This in order to 
               #give a correct input prioritizing format for the re.finditer which 
               #stores the output information in matches.
               s = ""
               re_or = "(" + s.join([x + "|" for x in dicts[cat]])[:-1] + ")"
               matches = [(cat, m.start(0), m.end(0)) for m in re.finditer(re_or, section)]

               if(len(matches) > 0):
                    for match in matches:
                         match_dict = {"id": match[0], "span":{"begin":match[1], "end":match[2]}, "obj":match[0]}
                         denotations.append(match_dict)
          denotated_sections.append(denotations)

     return denotated_sections, article

def generate_jsons(denotated_sections, article, path, metaf):
     '''
     Generates output json files. One file is generated for each section of an article.
     One file for the title, one for the abstract and one for each section of the body text.
     The files will be named based on their cord_uid and their section like follows:
     cord_uid-div_id-sectiontype.json
     eg:  31996494-0-title.json
          31996494-1-abstract.json
     '''
     [cord_uid, sourcedb, sourceid, obj] = read_meta(path_to_paper_id(path), metaf)
     for i in range(len(article)):
          text = article[i][0]
          section = article[i][1]
          denot = denotated_sections[i]

          json_data = {"cord_uid":cord_uid,
                         "sourcedb":sourcedb,
                         "sourceid":sourceid,
                         "div_id":i,
                         "text":text,
                         "denotations":denot
                         }
          with open(str(cord_uid) + "-" + str(i) + "-" + section + ".json", "w") as fp:
               json.dump(json_data, fp)


def main():
     articles_path = os.path.abspath("comm_use_subset_100") + "/"
     #articles_path = os.path.abspath("gold_standard_subset_10") + "/"

     articles = [f for f in listdir(articles_path) if isfile(join(articles_path, f))]

     metaf = "meta_subset_100.csv"
     #metaf = "gold_standard_subset_10.csv"

     setup_dicts("/home/jesper/EDAN70/classes")

     for f in articles:
          denot_sec, art = tag_article(articles_path + f, metaf)
          #generate_jsons(denot_sec, art, f, metaf)

if __name__ == '__main__':
     t0 = time.clock()
     main()
     t1 = time.clock() - t0
     print(t1)

     

