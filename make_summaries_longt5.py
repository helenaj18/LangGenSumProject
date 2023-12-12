# CODE IS BASED ON THIS: https://huggingface.co/google/long-t5-local-base - todo: breyta?
# CODE IS BASED ON THIS: https://huggingface.co/docs/transformers/v4.35.2/en/model_doc/longt5#transformers.LongT5ForConditionalGeneration
from transformers import AutoTokenizer, LongT5Model, LongT5ForConditionalGeneration
import glob
import os
import torch

# tokenizer = AutoTokenizer.from_pretrained("google/long-t5-local-base")
# model = LongT5Model.from_pretrained("google/long-t5-local-base")

tokenizer = AutoTokenizer.from_pretrained("Stancld/longt5-tglobal-large-16384-pubmed-3k_steps")
model = LongT5ForConditionalGeneration.from_pretrained(
    "Stancld/longt5-tglobal-large-16384-pubmed-3k_steps"
)

# NO GENDER
# Specify the folder path and file pattern
folder_path = 'Outputs/txt_files'
file_pattern = '*.txt'  # Example: List all .txt files

# Use glob to get a list of files that match the pattern
files = glob.glob(os.path.join(folder_path, file_pattern))

# Iterate over the files
for filename in files:
    summary_file_name = filename[:-4].replace("/txt_files/", "/summaries_legal_led/")+'.txt'
    new_summary_file_name = filename[:-4].replace("/txt_files/", "/summaries_longt5_CG/")+'.txt'
    if os.path.exists(summary_file_name) and not os.path.exists(new_summary_file_name):
        try:
            with open(filename) as file:
                txt_content = file.read()

            input = "Please summarize this article: " + txt_content
            inputs = tokenizer(input, return_tensors="pt")
            input_ids = inputs.input_ids
            
            with torch.no_grad():
                outputs = model.generate(input_ids, max_length=2048, no_repeat_ngram_size=10)
            
            summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

            with open(new_summary_file_name, 'w') as text_file:
                text_file.write(summary)
                print("Summarized: ", new_summary_file_name)
            
        except Exception as e:
            print("Could not summarize filename:\n " + filename[20:] + "because of exception: " + str(e))
    

# FEMALE
# Specify the folder path and file pattern
folder_path = 'Outputs/txt_files_female_only'
file_pattern = '*.txt'  # Example: List all .txt files

# Use glob to get a list of files that match the pattern
files = glob.glob(os.path.join(folder_path, file_pattern))

# Iterate over the files
for filename in files:
    summary_file_name = filename[:-4].replace("/txt_files_female_only/", "/summaries_legal_led/")+'.txt'
    new_summary_file_name = filename[:-4].replace("/txt_files_female_only/", "/summaries_longt5_CG_female_only/")+'.txt'
    if os.path.exists(summary_file_name) and not os.path.exists(new_summary_file_name):
        try:
            with open(filename) as file:
                txt_content = file.read()

            input = "Please summarize this article: " + txt_content
            inputs = tokenizer(input, return_tensors="pt")
            input_ids = inputs.input_ids
            
            with torch.no_grad():
                outputs = model.generate(input_ids, max_length=2048, no_repeat_ngram_size=10)
            
            summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

            with open(new_summary_file_name, 'w') as text_file:
                text_file.write(summary)
                print("Summarized: ", new_summary_file_name)
            
        except Exception as e:
            print("Could not summarize filename:\n " + filename[20:] + "because of exception: " + str(e))
    

# MALE
# Specify the folder path and file pattern
folder_path = 'Outputs/txt_files_male_only'
file_pattern = '*.txt'  # Example: List all .txt files

# Use glob to get a list of files that match the pattern
files = glob.glob(os.path.join(folder_path, file_pattern))
 
for filename in files:
    summary_file_name = filename[:-4].replace("/txt_files_male_only/", "/summaries_legal_led/")+'.txt'
    new_summary_file_name = filename[:-4].replace("/txt_files_male_only/", "/summaries_longt5_CG_male_only/")+'.txt'
    if os.path.exists(summary_file_name) and not os.path.exists(new_summary_file_name):
        try:
            with open(filename) as file:
                txt_content = file.read()

            input = "Please summarize this article: " + txt_content
            inputs = tokenizer(input, return_tensors="pt")
            input_ids = inputs.input_ids
            
            with torch.no_grad():
                outputs = model.generate(input_ids, max_length=2048, no_repeat_ngram_size = 10)
            
            summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

            with open(new_summary_file_name, 'w') as text_file:
                text_file.write(summary)
                print("Summarized: ", new_summary_file_name)
            
        except Exception as e:
            print("Could not summarize filename:\n " + filename[20:] + "because of exception: " + str(e))
    



