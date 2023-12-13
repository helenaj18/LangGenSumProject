import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from itertools import combinations
import glob
import os


### START: https://www.kaggle.com/code/samuelcortinhas/nlp3-bag-of-words-and-similarity/notebook
def cosine_sim(a,b):
    return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))
### END: https://www.kaggle.com/code/samuelcortinhas/nlp3-bag-of-words-and-similarity/notebook


def get_corpus(filename, model_name, gender):
    corpus = []
    for i in range(10):
        file = model_name + gender + str(i) + "/" + filename

        with open(file) as f:
            summary = f.read()
            corpus.append(summary)
    
    return corpus

def calculate_similarity(corpus):
    similarity_score = {}
    vectorizer = CountVectorizer()
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

N = 20 # There are 20 transcripts for each gender and model

files = glob.glob(os.path.join('Outputs/gendered/female_only0', '*.txt'))

filenames = []
for filename in files:
    filenames.append(filename.split("/")[-1])

led_base_f_similarity= {}
led_base_m_similarity = {}
legal_led_f_similarity = {}
legal_led_m_similarity = {}
longt5_f_similarity = {}
longt5_m_similarity = {}

for file in filenames:
    led_base_f_corpus = get_corpus(file, 'Outputs/gendered_summaries_led_base/', 'female_only') # as the average similarity between summaries generated for the same group as i on the same original document
    led_base_f_similarity[file] = calculate_similarity(led_base_f_corpus)
    led_base_m_corpus= get_corpus(file, 'Outputs/gendered_summaries_led_base/', 'male_only') # as the average similarity with summaries generated for the other group.
    led_base_m_similarity[file] = calculate_similarity(led_base_m_corpus)
    
    legal_led_f_corpus = get_corpus(file, 'Outputs/gendered_summaries_legal_led/', 'female_only')
    legal_led_f_similarity[file] = calculate_similarity(legal_led_f_corpus)
    legal_led_m_corpus = get_corpus(file, 'Outputs/gendered_summaries_legal_led/', 'male_only')
    legal_led_m_similarity[file] = calculate_similarity(legal_led_m_corpus)

    longt5_f_corpus = get_corpus(file, 'Outputs/gendered_summaries_longt5_CG/', 'female_only')
    longt5_f_similarity[file] = calculate_similarity(longt5_f_corpus)
    longt5_m_corpus = get_corpus(file, 'Outputs/gendered_summaries_longt5_CG/', 'male_only')
    longt5_m_similarity[file] = calculate_similarity(longt5_m_corpus)


sum_items_f = []
sum_items_m = []
for file in filenames:
    if led_base_f_similarity[file] > led_base_m_similarity[file]:
        sum_items_f.append(1)
    else:
        sum_items_f.append(0)
    
    if led_base_m_similarity[file] > led_base_f_similarity[file]:
        sum_items_m.append(1)
    else:
        sum_items_m.append(0)

f_score = 2 * np.sum(sum_items_f) / N - 1
m_score = 2 * np.sum(sum_items_m) / N - 1


print("LED BASE REPRESENTATION BIAS")
print("FEMALE: ", f_score)
print("MALE: ", m_score)



sum_items_f = []
sum_items_m = []
for file in filenames:
    if legal_led_f_similarity[file] > legal_led_m_similarity[file]:
        sum_items_f.append(1)
    else:
        sum_items_f.append(0)
    
    if legal_led_m_similarity[file] > legal_led_f_similarity[file]:
        sum_items_m.append(1)
    else:
        sum_items_m.append(0)

f_score = 2 * np.sum(sum_items_f) / N - 1
m_score = 2 * np.sum(sum_items_m) / N - 1

print("---------------------")
print("LEGAL LED REPRESENTATION BIAS")
print("FEMALE: ", f_score)
print("MALE: ", m_score)





sum_items_f = []
sum_items_m = []
for file in filenames:
    if longt5_f_similarity[file] > longt5_m_similarity[file]:
        sum_items_f.append(1)
    else:
        sum_items_f.append(0)
    
    if longt5_m_similarity[file] > longt5_f_similarity[file]:
        sum_items_m.append(1)
    else:
        sum_items_m.append(0)

f_score = 2 * np.sum(sum_items_f) / N - 1
m_score = 2 * np.sum(sum_items_m) / N - 1


print("---------------------")
print("LONG T5 REPRESENTATION BIAS")
print("FEMALE: ", f_score)
print("MALE: ", m_score)



