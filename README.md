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

## Data downloading/Generation/Preprocessing
This section describes the files used to scrape SeekingAlpha and generate the summaries. 

### GetTickers.py

### Scraper.py

### Transcripts.py

### make_summaries.py

## Make_summaries_alpaca.py


## make_summaries_longt5.py


### create_datasets.py
This function was used to create datasets of summaries with only male names and only female names, two seperate datasets for each model. Can be run in the Code folder in the following way:

```
python3 create_datasets.py
```

### html_to_txt.py
This file was used to change html content from the webscraping to txt content

### file_checker.py
This file was just used to check how many files were in the summary folder, to see how much data had been gathered when running the make_summaries.py function. Run like this:

```
python3 create_datasets.py
```


## Training the baselines
This section describes the functions used to train the baselines (ATH á ég að vera með þetta?)

## Experiments
This section describes the files used to do the experiments

## Evaluations

### mean_ppl.py

### avg_length_data.py 
Used to calculate the average length of the summaries. The string "folder_path" was changed to account for summaries of different models. This code is run in this way, in the Code folder:
```
python3 avg_length_data.py
```
## inclusion_bias.py

## sentiment_analysis.py


----
## data_gathering.ipynb - TODO: eyða?


