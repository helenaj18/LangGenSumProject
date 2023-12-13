
legal_perplexity_file_name = 'Outputs/perplexity/perplexity_legal_led.txt'

perplexity_file_name = 'Outputs/perplexity/perplexity.txt'

longt5_file_name = 'Outputs/perplexity/longt5_CG.txt'

filenames = [legal_perplexity_file_name, perplexity_file_name, longt5_file_name]

lowest_ppl_dict = {}
highest_ppl_dict = {}
mean_ppl = {}
highest_ppl = 0
lowest_ppl = 100000
for file in filenames:
    with open(file, "r") as f:
        total_ppl = 0
        for count, line in enumerate(f):
            _, ppl = line.strip().split(";; ")
            ppl = float(ppl)
            if ppl < lowest_ppl:
                lowest_ppl = ppl
            if ppl > highest_ppl:
                highest_ppl = ppl
            total_ppl += ppl

    file = file.split("/")
    mean_ppl[file[-1]] = total_ppl/(count+1)
    lowest_ppl_dict[file[-1]] = lowest_ppl
    highest_ppl_dict[file[-1]] = highest_ppl


print(filenames)
print(mean_ppl)
print(lowest_ppl_dict)
print(highest_ppl_dict)