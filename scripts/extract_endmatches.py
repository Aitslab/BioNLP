# author: Sonja Aits
    
# this function extracts all words in the inputfile that end on a specific substring to the outputfile
# the matches are listed in lowercase and alphabetically sorted

def extract_endmatches(inputfile, substring, outputfile):

    # Open the text file for reading
    with open(inputfile, 'r') as file:
        # Read the file content into a string
        file_contents = file.read()

    # Split the file content into a list of words
    words = file_contents.split()

     # Initialize an empty list to store the detected words
    matches = []

    # Loop through each word in the list and check if it ends with the substring
    for word in words:
        if word.endswith(substring):
            # Add it to the matches list
            matches.append(word)
    
    # convert all items in matches list to lower case
    matches_lowercase = [x.lower() for x in matches]
                         
    # remove duplicates by converting to a set
    matches_set = set(matches_lowercase)

    # Print the results to screen and file in alphabetic order
    print('Words ending with '+substring+':')
    for x in sorted(matches_set):
        print(x)

    with open(outputfile, 'w') as f:
        for y in sorted(matches_set):
           f.write(y+'\n')
