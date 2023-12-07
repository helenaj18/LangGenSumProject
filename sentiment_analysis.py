from textblob import TextBlob
import glob
import os
import nltk
nltk.download('punkt')

# Specify the folder path and file pattern
folder_path = 'Outputs/summaries_led_base'
file_pattern = '*.txt'  # Example: List all .txt files

# Use glob to get a list of files that match the pattern
files = glob.glob(os.path.join(folder_path, file_pattern))

sentiment = {}
for filename in files:
    summary_polarity = 0
    with open(filename, "r") as file:
        summary = file.read()

    blob = TextBlob(summary)
    blob.tags           # [('The', 'DT'), ('titular', 'JJ'),
                        #  ('threat', 'NN'), ('of', 'IN'), ...]

    blob.noun_phrases   # WordList(['titular threat', 'blob',
                        #            'ultimate movie monster',
                        #            'amoeba-like mass', ...])

    for sentence in blob.sentences:
        summary_polarity += sentence.sentiment.polarity
    
    sentiment[filename[:-4].split("/")[-1]] = summary_polarity/len(blob.sentences)

# print(sentiment)

avg_sentiment = sum(sentiment.values())/len(sentiment)
print(avg_sentiment)