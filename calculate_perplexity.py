from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import glob
import os

def calculate_perplexity():
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    tokenizer = AutoTokenizer.from_pretrained("gpt2")

    # Specify the folder path and file pattern
    folder_path = 'Outputs/summaries_longt5_CG'
    # folder_path = 'Outputs/summaries_legal_led'
    file_pattern = '*.txt'   

    # Use glob to get a list of files that match the pattern
    files = glob.glob(os.path.join(folder_path, file_pattern))
    perplexity_file_name = 'Outputs/perplexity/longt5_CG.txt'

    # perplexity_file_name = 'Outputs/perplexity/perplexity_legal_led.txt'


    for filename in files:
        # You can perform operations on each file here
        # For example, print the file name
        with open(filename) as file:
            summary = file.read()

        try:
            inputs = tokenizer(summary, return_tensors = "pt")
            loss = model(input_ids = inputs["input_ids"], labels = inputs["input_ids"]).loss
            ppl = torch.exp(loss)

            with open(perplexity_file_name, 'a') as ppl_file:
                return_str = filename + ";; " + str(ppl.item()) + '\n'
                ppl_file.write(return_str)
        except:
            with open(perplexity_file_name, 'a') as ppl_file:
                return_str = filename + ";; " + str(ppl.item()) + '\n'
                ppl_file.write("None")


calculate_perplexity()