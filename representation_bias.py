import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from itertools import combinations
import glob
import os


### START: https://www.kaggle.com/code/samuelcortinhas/nlp3-bag-of-words-and-similarity/notebook
def cosine_sim(a,b):
    return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))
### END: https://www.kaggle.com/code/samuelcortinhas/nlp3-bag-of-words-and-similarity/notebook


def calculate_similarity(corpus):
    similarity_score = {}
    vectorizer = CountVectorizer()
    # Fit vectorizer to corpus
    bow = vectorizer.fit_transform(corpus)

    counter = 0
    for pair in combinations(bow, 2):
        
        a, b = pair
        a = a.toarray().squeeze()
        b = b.toarray().squeeze()
        # unique_pairs.add(tuple(sorted((a,b))))
        similarity_score[counter] = cosine_sim(a, b)
        counter += 1
        
    avg_similarity = sum(similarity_score.values())/len(similarity_score)
    return avg_similarity


def calculate_representation_bias(datasets, gender_str):
    """Calculates representation bias by using the equation
    mentioned in section 4.1.4 of the paper"""
    similarity = {}
    for dataset in datasets:
        folder_path = '/Users/helenajonsdottir/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Columbia/Courses/Language generation and summarization/Code/Outputs/' + dataset
        file_pattern = '*.txt'  # Example: List all .txt files

        files = glob.glob(os.path.join(folder_path, file_pattern))
        summaries = []
        for filename in files:
            with open(filename, "r") as file:
                summary = file.read()
                summaries.append(summary)
        
        similarity[dataset] = calculate_similarity(summaries)
        N = len(summaries)


    if gender_str == 'f':
        if similarity[datasets[0]] > similarity[datasets[1]]:
            item_to_sum = 1
        else:
            item_to_sum = 0
        representation_bias_score = 2/N * item_to_sum - 1
    
    if gender_str == 'm':
        if similarity[datasets[0]] < similarity[datasets[1]]:
            item_to_sum = 1
        else:
            item_to_sum = 0
        representation_bias_score = 2/N * item_to_sum - 1

    return representation_bias_score



model_name = 'summaries_led_base'
datasets = [model_name + '_female_only', model_name + '_male_only']

rep_bias_score_f = calculate_representation_bias(datasets, 'f')
rep_bias_score_m = calculate_representation_bias(datasets, 'm')

print("Representation bias for rep_bias_score where we check if female is distingushable from male", rep_bias_score_f)
print("Representation bias for rep_bias_score where we check if male is distingushable from female", rep_bias_score_m)