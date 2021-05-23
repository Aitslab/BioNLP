import re
import random
import fileinput
import glob
import pandas as pd

def singlereplace(startlist, replaced1, synonyms1, filename):
  #startlist should contain list of phrases that serve as starting point
  #synonyms1 and synonyms2 should be list of phrases used for replacement
  #replaced1 anfd replaced2 should be strings to be replaced
  #filename is name of output file

  list1 = []

  for item in startlist:
    for synonym1 in synonyms1:
      new = item.replace(replaced1, synonym1)
      list1.append(new)
  list1 = list(set(list1)) #removes duplicates
  print(len(list1))

  with open(filename, 'a', encoding='utf-8') as file:
    for item in list1:
      file.write(item+'\n')

def doublereplace(startlist, replaced1, replaced2, synonyms1, synonyms2, filename):
  #startlist should contain list of phrases that serve as starting point
  #synonyms1 and synonyms2 should be list of phrases used for replacement
  #replaced1 anfd replaced2 should be strings to be replaced
  #filename is name of output file

  list1 = []
  list2 = []
  list3 = []
  
  for item in startlist:
    for synonym1 in synonyms1:
      new = item.replace(replaced1, synonym1)
      list1.append(new)

  for item in list1:
    for synonym2 in synonyms2:
      new = item.replace(replaced2, synonym2)
      list2.append(new)
  list2 = list(set(list2))

  for item in list2:
    new3 = item.replace(' ,', ',')
    list3.append(new3)
  list3 = list(set(list3))
  print(len(list3))

  with open(filename, 'a', encoding='utf-8') as file:
    for item in list3:
      file.write(item+'\n')

def triplereplace(startlist, replaced1, replaced2, replaced3, synonyms1, synonyms2, synonmys3, filename):
  #startlist should contain list of phrases that serve as starting point
  #synonyms* should be lists of phrases used for replacement
  #replaced* should be strings to be replaced
  #filename is name of output file

  list1 = []
  list2 = []
  list3 = []
  list4 = []

  for item in startlist:
    for synonym1 in synonyms1:
      new1 = item.replace(replaced1, synonym1)
      list1.append(new1)

  for item in list1:
    for synonym2 in synonyms2:
      new2 = item.replace(replaced2, synonym2)
      list2.append(new2)

  for item in list2:
    for synonym3 in synonyms3:
      new3 = item.replace(replaced3, synonym3)
      list3.append(new3)
  
  for item in list3:
    new4 = item.replace(' ,', ',')
    list4.append(new4)
  list4 = list(set(list4))
  print(len(list4))

  with open(filename, 'a', encoding='utf-8') as file:
    for item in list4:
      file.write(item+'\n')

def quadreplace(startlist, replaced1, replaced2, replaced3, replaced4, synonyms1, synonyms2, synonmys3, synonyms4, filename):
  #startlist should contain list of phrases that serve as starting point
  #synonyms* should be lists of phrases used for replacement
  #replaced* should be strings to be replaced
  #filename is name of output file

  list1 = []
  list2 = []
  list3 = []
  list4 = []
  list5 = []

  for item in startlist:
    for synonym1 in synonyms1:
      new1 = item.replace(replaced1, synonym1)
      list1.append(new1)

  for item in list1:
    for synonym2 in synonyms2:
      new2 = item.replace(replaced2, synonym2)
      list2.append(new2)

  for item in list2:
    for synonym3 in synonyms3:
      new3 = item.replace(replaced3, synonym3)
      list3.append(new3)

  for item in list3:
    for synonym4 in synonyms4:
      new4 = item.replace(replaced4, synonym4)
      list4.append(new4)
  
  for item in list4:
    new5 = item.replace(' ,', ',')
    list5.append(new5)
  list5 = list(set(list5))
  print(len(list5))

  with open(filename, 'a', encoding='utf-8') as file:
    for item in list5:
      file.write(item+'\n')