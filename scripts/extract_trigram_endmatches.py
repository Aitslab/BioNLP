# author: Sonja Aits

# this function extracts all word triplets (trigrams) in the inputfile that end on a specific word to the outputfile
# the matches are listed in lowercase and alphabetically sorted

def extract_trigram_endmatches(inputfile, endword, outputfile):

    # Open the text file for reading
    with open(inputfile, 'r') as file:
        # Read the file content into a string
        file_contents = file.read()
    
    # Split the file content into a list of words
    words = file_contents.split()
    
    # Initialize an empty list to store matches
    matches = []

    # Loop through the list of strings
    for i in range(len(words) - 2):
    
    # Check if the last string item is 'death'
        if words[i+2] == endword:
            # Merge the three string items with a blank in between
            merged_string = ' '.join([words[i], words[i+1], words[i+2]])

            # Append the merged string to the list of matches
            matches.append(merged_string)
    
    # convert all items in matches list to lower case
    matches_lowercase = [x.lower() for x in matches]
                         
    # remove duplicates by converting to a set
    matches_set = set(matches_lowercase)

    # Print the results to screen and file in alphabetic order
    print('Trigrams ending on '+endword+':')
    for x in sorted(matches_set):
        print(x)

    with open(outputfile, 'w') as f:
        for y in sorted(matches_set):
           f.write(y+'\n')
