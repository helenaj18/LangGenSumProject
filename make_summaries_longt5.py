from transformers import AutoTokenizer, LongT5Model
import glob
import os

tokenizer = AutoTokenizer.from_pretrained("google/long-t5-local-base")
model = LongT5Model.from_pretrained("google/long-t5-local-base")

# Specify the folder path and file pattern
folder_path = '/Users/helenajonsdottir/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Columbia/Courses/Language generation and summarization/Code/Outputs/txt_files'
file_pattern = '*.txt'  # Example: List all .txt files

# Use glob to get a list of files that match the pattern
files = glob.glob(os.path.join(folder_path, file_pattern))

# Iterate over the files
for filename in files:
    # You can perform operations on each file here
    # For example, print the file name
    with open(filename) as file:
        txt_content = file.read()

    input = "Please summarize this article: " + txt_content
    inputs = tokenizer(input, return_tensors="pt")
    outputs = model(**inputs) # TODO fix this to work!!
    print(outputs)

