# CODE IS BASED ON THIS: https://huggingface.co/google/long-t5-local-base 
# CODE IS BASED ON THIS: https://huggingface.co/docs/transformers/v4.35.2/en/model_doc/longt5#transformers.LongT5ForConditionalGeneration
from transformers import AutoTokenizer, LongT5Model, LongT5ForConditionalGeneration
import glob
import os
import torch

tokenizer = AutoTokenizer.from_pretrained("Stancld/longt5-tglobal-large-16384-pubmed-3k_steps")
model = LongT5ForConditionalGeneration.from_pretrained(
    "Stancld/longt5-tglobal-large-16384-pubmed-3k_steps"
)

for counter in range(10):
    # FEMALE
    # Specify the folder path and file pattern
    folder_path = 'Outputs/gendered/female_only' + str(counter) + '/'
    file_pattern = '*.txt'   

    # Use glob to get a list of files that match the pattern
    files = glob.glob(os.path.join(folder_path, file_pattern))

    # Iterate over the files
    for filename in files:
        summary_file_name = filename[:-4].replace("/gendered/female_only"+ str(counter) + '/', "/summaries_legal_led/")+'.txt'
        new_summary_file_name = filename[:-4].replace('/gendered/female_only' + str(counter) + '/', "/gendered_summaries_longT5_CG/female_only" + str(counter) + "/")+'.txt'
        new_dir = new_summary_file_name.split("A")[0]
        # Check whether the specified path exists or not
        if not os.path.exists(new_dir):
            # Create a new directory because it does not exist
            os.makedirs(new_dir)

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
        

for counter in range(10):
    # MALE
    # Specify the folder path and file pattern
    folder_path = 'Outputs/gendered/male_only'+ str(counter) + '/'
    file_pattern = '*.txt'   

    # Use glob to get a list of files that match the pattern
    files = glob.glob(os.path.join(folder_path, file_pattern))
    
    for filename in files:
        summary_file_name = filename[:-4].replace('/gendered/male_only' + str(counter) + '/', "/summaries_legal_led/")+'.txt' 
        new_summary_file_name = filename[:-4].replace('/gendered/male_only' + str(counter) + '/', "/gendered_summaries_longt5_CG/male_only" + str(counter) + "/")+'.txt'
        new_dir = new_summary_file_name.split("A")[0]
        # Check whether the specified path exists or not
        if not os.path.exists(new_dir):
            # Create a new directory because it does not exist
            os.makedirs(new_dir)
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
        



