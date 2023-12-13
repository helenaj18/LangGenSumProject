# Repository for Language generation and Summarization semester project
Helena Jonsdottir, hsj2115

## Sources of code
The code in the folder SeekingAlpha-Scraper is from this repository: https://github.com/hamid-vakilzadeh/SeekingAlpha-Scraper
It was used to scrape data from the Seeking Alpha website: https://seekingalpha.com/
However, these file located within that folder were added by me:
- GetTicker.py
- secret.yaml
- listing_status.csv - this data was gotten from Alpha Vantage, https://www.alphavantage.co/documentation/ 

This is the License for the Repository:

BSD 2-Clause License

Copyright (c) 2022, Hamid Vakilzadeh

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


# List of files and description of what they are used for
All python files can be run like this in the code folder unless otherwise specified:
```
python3 <name_of_file.py>
```

## Data downloading/Generation/Preprocessing
This section describes the files used to scrape SeekingAlpha and generate the summaries. 

### GetTickers.py
This file gets the tickers needed for the web scraping. It does so by taking tickers for publicly listed companies, using the listing_status.csv file gotten from Alpha Vantage. These symbols are then used to webscrape Seeking Alpha for each of the symbols. This was done for about 2000 companies and html files were the output.

### Scraper.py
This file scrapes the data from Seeking alpha

### Transcripts.py
This file assists Scraper.py to collect the data scraped in a nice way.

### html_to_txt.py
This file was used to change html content from the webscraping to txt content to be able to make summaries. I ended up with 203 text transcripts and then stopped because that was enough. Two target html classes were used to get the transcript text and no unnecessary data like html tags.

### make_summaries.py
This file is used to make summaries for the LED-base and LED-legal models. The model and tokenizer variables are changed to fit each model before the run.

### make_summaries_longt5_CG.py
This file is used to make summaries for the Long T5 model.


### create_datasets.py
This file was used to create datasets of 20 transcripts with only male names and only female names, but with 10 instances of each transcript with random names selected for each one. Can be run in the Code folder in the following way:


### make_gendered_summaries_led_base
This file was used to make summaries from the gendered transcripts in Outputs/gendered (Female and male) for the LED-base model

### make_gendered_summaries_legal_led
This file was used to make summaries from the gendered transcripts in Outputs/gendered (Female and male) for the Legal LED model

### make_gendered_summaries_longt5
This file was used to make summaries from the gendered transcripts in Outputs/gendered (Female and male) for the Long T5 model

### file_checker.py
This file was just used to check how many files were in the summary folder, to see how much data had been gathered when running the make_summaries files. 

## Outputs
All data can be found under /Outputs where:
- Transcripts: Includes html transcripts scraped from SeekingAlpha
- txt_files: Includes txt files obtained from the html files
- gendered: Includes 10 versions of each of the 20 transcripts used to make the gendered datasets, for both genders
- gendered_summaries_led_base, gendered_summaries_legal_led, gendered_summaries_longt5_CG: The genderd summaries generated from the transcripts in /gendered
- perplexity: Contains files with the perplexity score for all summaries for each model. This was used to calculate mean perplexity.
- summaries_led_base, summaries_legal_led, summaries_longt5CG: Contain summaries generated from the transcripts in txt_files 


## Experiments and Evaluation
This section describes the files used to do the experiments

### evaluation.py
This function combines multiple experiments and evaluations in one file. The *folder_path* string can be changed to check for other models. It calculates inclusion bias, hallucination bias, representation bias, sentiment, perplexity, word list ratios, name list ratios, and hallucunation ratios.

### avg_length_data.py 
Used to calculate the average length of the summaries. The string *folder_path* was changed to account for summaries of different models. 

### mean_ppl.py
This file calculates the mean, lowest and highest perplexity over all the summaries of a all models. 

### statistical.py
This file calculates whether the statistical difference between two numbers is significant.

### sentiment_analysis.py
This function calculates the average sentiment of all summaries for each model. The *folder_path* is changed to include different models. The sentiment is calculated using TextBlob: https://textblob.readthedocs.io/en/dev/




