### THIS CODE IS TAKEN FROM HERE: https://huggingface.co/chainyo/alpaca-lora-7b
import torch
from transformers import GenerationConfig, LlamaTokenizer, LlamaForCausalLM
import glob
import os

def generate_prompt(instruction: str, input_ctxt: str = None) -> str:
    if input_ctxt:
        return f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{instruction}

### Input:
{input_ctxt}

### Response:"""
    else:
        return f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
{instruction}

### Response:"""



tokenizer = LlamaTokenizer.from_pretrained("chainyo/alpaca-lora-7b")
model = LlamaForCausalLM.from_pretrained(
    "chainyo/alpaca-lora-7b",
    load_in_8bit=True,
    torch_dtype=torch.float16,
    device_map="auto",
)
generation_config = GenerationConfig(
    do_sample = True,
    temperature=0.2,
    top_p=0.75,
    top_k=40,
    num_beams=4,
    max_new_tokens=128,
)

model.eval()
if torch.__version__ >= "2":
    model = torch.compile(model)
## END OF CODE SEGMENT FROM HERE: https://huggingface.co/chainyo/alpaca-lora-7b

# Specify the folder path and file pattern
folder_path = 'Outputs/txt_files'
file_pattern = '*.txt'  # Example: List all .txt files

# Use glob to get a list of files that match the pattern
files = glob.glob(os.path.join(folder_path, file_pattern))


for filename in files:
    summary_file_name = filename[:-4].replace("/txt_files/", "/summaries_legal_led/")+'.txt'
    new_summary_file_name = filename[:-4].replace("/txt_files/", "/summaries_alpaca_lora/")+'.txt'
    if os.path.exists(summary_file_name) and not os.path.exists(new_summary_file_name):
        try: 
            ### THIS CODE IS TAKEN FROM HERE: https://huggingface.co/chainyo/alpaca-lora-7b
            instruction = "Summarize the text in the input."

            with open(filename) as file:
                input_ctxt = file.read()

            prompt = generate_prompt(instruction, input_ctxt)
            input_ids = tokenizer(prompt, return_tensors="pt").input_ids
            input_ids = input_ids.to(model.device)

            with torch.no_grad():
                outputs = model.generate(
                    input_ids=input_ids,
                    generation_config=generation_config,
                    return_dict_in_generate=True,
                    output_scores=True,
                )

            response = tokenizer.decode(outputs.sequences[0], skip_special_tokens=True)
            ### END OF CODE SEGMENT FROM HERE: https://huggingface.co/chainyo/alpaca-lora-7b
            with open(new_summary_file_name, "w") as f:
                f.write(response)
        except Exception as e:
            print("Could not summarize filename:\n " + filename[20:] + "because of exception: " + str(e))