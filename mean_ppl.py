
legal_perplexity_file_name = 'Outputs/perplexity/perplexity_legal_led.txt'

perplexity_file_name = 'Outputs/perplexity/perplexity.txt'

filenames = [legal_perplexity_file_name, perplexity_file_name]

mean_ppl = {}
for file in filenames:
    with open(file, "r") as f:
        total_ppl = 0
        for count, line in enumerate(f):
            _, ppl = line.strip().split(";; ")
            total_ppl += float(ppl)

    file = file.split("/")
    mean_ppl[file[-1]] = total_ppl/(count+1)


print(mean_ppl)