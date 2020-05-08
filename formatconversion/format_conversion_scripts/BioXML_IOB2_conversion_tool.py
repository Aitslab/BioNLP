## This script is written for converting BioC.xml format to IOB2 format
## For running you only need to give two input and output files as input to the script
## Running should be in the form of "python BioXML_IOB2_conversion_tool.py input_file output_file"

import collections
import csv
import sys
import codecs
from xml.dom.minidom import parse
import xml.dom.minidom
from bs4 import BeautifulSoup

##start by define the first function
def read_and_parse_input_xml(file_name):

    file = codecs.open(file_name, "r", "utf-8")
    soup = BeautifulSoup(file, "html.parser")
	
    return soup

       
def tokenize_text(passage):
     ### Because I used split for spliting all the tokens I had to add space among words and puncutation signs 
    main_text = passage.find('text').text
    main_text = main_text.replace(',',' , ')
    main_text = main_text.replace(':',' : ')
    main_text = main_text.replace(';',' ; ')
    main_text = main_text.replace('(',' ( ')
    main_text = main_text.replace(')',' ) ')
    main_text = main_text.replace('.',' . ')
    main_text = main_text.replace('%',' % ')
    main_text = main_text.replace('[',' [ ')
    main_text = main_text.replace(']',' ] ') 
    tokens = main_text.split()
    return tokens


    ##########################################################
    ### Annotations blocks are NEs that the tag is presneted in the infon block 
def extract_words_from_passage(passage):
    annot = passage.find_all('annotation')
    words_per_pass = []
    for j in annot:
        info = j.find_all('infon')
        for k in info:
            if "key=\"type\"" in str(k):
                words_per_pass.append([j.find('text').text, k.text])
                
    return words_per_pass
    #######################################################
def convert_words_tags_to_IOB2(tokens,words_per_pass, IOB2_list):
    tokenCtr = 0
    while tokenCtr < len(tokens):
        isFound = False
        for wpp in words_per_pass:
            words = wpp[0].split()
            tags  = wpp[1]
            if tokens[tokenCtr:tokenCtr+len(words)] == words:
                isFound = True
                for tok in tokens[tokenCtr:tokenCtr+len(words)]:
                    if tok is tokens[tokenCtr]:
                        IOB2_list.append([tok,'B-'+ wpp[1]])
                    else:
                        IOB2_list.append([tok,'I-'+ wpp[1]])
                
                tokenCtr += len(words)-1
                break
        if not isFound:
            IOB2_list.append([tokens[tokenCtr],'O'])
        tokenCtr += 1

    return IOB2_list
###################################################
def write_to_IOB2_format(iob2_list, file_name):
    IOB2_file = open(file_name, 'w')
          
    for line in iob2_list:
        if line[0] == '.':
            print('\n',file=IOB2_file)
        else:
            print(line[0], line[1], sep=' ',file=IOB2_file)
            
    IOB2_file.close()
##################################################
def main():

    in_xml_file   = sys.argv[1]
    out_iob2_file = sys.argv[2]

    soup = read_and_parse_input_xml(in_xml_file)
    passages = soup.find_all('passage')
    IOB2_list =[]
    
### First we need to find all passages in the xml file which annotations are inside a "passage" block
    for i in passages:
        words_per_pass    = extract_words_from_passage(i)
        tokens            = tokenize_text(i)
        IOB2_list         = convert_words_tags_to_IOB2(tokens,words_per_pass, IOB2_list)
        print(IOB2_list)
    write_to_IOB2_format(IOB2_list, out_iob2_file)   
    

if __name__ == '__main__':
    main()

