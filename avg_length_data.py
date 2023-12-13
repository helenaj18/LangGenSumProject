import glob
import os

# Specify the folder path and file pattern
folder_path = 'Outputs/summaries_longt5_CG'
file_pattern = '*.txt'   

# Use glob to get a list of files that match the pattern
files = glob.glob(os.path.join(folder_path, file_pattern))

length = {}
no_of_words = {}
for filename in files:
    with open(filename) as file:
        summary = file.read()
    

    length[file] = len(summary)
    no_of_words[file] = len(summary.split(" "))

avg_length = sum(length.values())/len(length)
avg_no_of_words = sum(no_of_words.values())/len(no_of_words)

print("Avg length for longT5 summaries in characters: ", avg_length)
print("Avg no of words for longT5 summaries in words: ", avg_no_of_words)