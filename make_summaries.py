import glob
import os
import torch
from transformers import AutoTokenizer, LEDForConditionalGeneration, LEDTokenizer

# START: Code for the model was found here: https://huggingface.co/docs/transformers/model_doc/led and here: https://huggingface.co/nsi319/legal-led-base-16384


model = LEDForConditionalGeneration.from_pretrained("allenai/led-large-16384-arxiv")

# model = LEDForConditionalGeneration.from_pretrained("nsi319/legal-led-base-16384")
tokenizer = AutoTokenizer.from_pretrained("allenai/led-large-16384-arxiv")

# Specify the folder path and file pattern
folder_path = 'Outputs/txt_files'
file_pattern = '*.txt'  # Example: List all .txt files

# Use glob to get a list of files that match the pattern
files = glob.glob(os.path.join(folder_path, file_pattern))

# Iterate over the files
for filename in files:
    with open(filename) as file:
        txt_content = file.read()
    
    summary_file_name = filename[:-4].replace("/txt_files/", "/summaries_legal_led/")+'.txt'
    new_summary_file_name = filename[:-4].replace("/txt_files/", "/summaries/")+'.txt'
    if os.path.exists(summary_file_name):
        try: 
            inputs = tokenizer.encode(txt_content, return_tensors="pt")
            global_attention_mask = torch.zeros_like(inputs)
            global_attention_mask[:, 0] = 1
            summary_ids = model.generate(inputs, global_attention_mask=global_attention_mask, num_beams=3, max_length=2048, no_repeat_ngram_size=10)
            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
            # TODO: add this parameter so I don't get repeats, if I find it: no repeat n-gram parameter
            with open(new_summary_file_name, 'w') as text_file:
                text_file.write(summary)
                print("Summarized: ", new_summary_file_name)
        except Exception as e:
            print("Could not summarize filename:\n " + filename[20:] + "because of exception: " + str(e))


# END: Code for the model was found here: https://huggingface.co/docs/transformers/model_doc/led and here: https://huggingface.co/nsi319/legal-led-base-16384