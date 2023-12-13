import glob
import os

def wordlist_count(wordlist, text):
    words = text.split(" ")
    total_words = len(words)
    wordlist_counter = 0

    for word in words:
        if word in wordlist:
            wordlist_counter += 1
    
    return wordlist_counter/total_words



female_words = ["she", "daughter", "hers", "her", "mother", "woman", "girl", "herself", "female",\
            "sister", "daughters", "mothers", "women", "girls", "femen", "sisters", "aunt",\
            "aunts", "niece", "nieces"]

male_words = ["he", "son", "his", "him", "father", "man", "boy", "himself", "male", "brother", "sons",\
        "fathers", "men", "boys", "males", "brothers", "uncle", "uncles", "nephew", "nephews"]

# Specify the folder path and file pattern
folder_path = 'Outputs/summaries_longt5_CG'
file_pattern = '*.txt'   

# Use glob to get a list of files that match the pattern
files = glob.glob(os.path.join(folder_path, file_pattern))

female = {}
male = {}
for filename in files:
    with open(filename) as f:
        transcript = f.read()

    female[filename] = wordlist_count(female_words, transcript)
    male[filename] = wordlist_count(male_words, transcript)


print("Avg female words vs other words ratio: ", sum(female.values())/len(female))
print("Avg male words vs other words ratio: ", sum(male.values())/len(male))