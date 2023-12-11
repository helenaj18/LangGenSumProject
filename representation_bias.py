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


def calculate_similarity(main_corpus, other_corpus):
    similarity_compared_to_own_gender = {}
    similarity_compared_to_other_gender = {}
    similarity_list = []
    similarity_list_other = []
    N = 203 # There are 203 summaries for each gender and each model

    # TODO: check similarity between summary generated for male
    # and summary generated for female

    for key, main_summary in main_corpus.items():
        other_summary = other_corpus[key.replace('female', 'male')]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([main_summary, other_summary])
        similarity_matrix = cosine_similarity(tfidf_matrix)
        cosine_similarity_value = similarity_matrix[0, 1]
        similarity_list.append(cosine_similarity_value)
    
    avg_similarity = sum(similarity_list)/len(similarity_list)
    print(avg_similarity)


    # Calculate average similarity between summaries of the same gender
    for main_summary_name, main_summary in main_corpus.items():
        for summary_2_name, summary_2 in main_corpus.items():
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform([main_summary, summary_2])
            similarity_matrix = cosine_similarity(tfidf_matrix)
            cosine_similarity_value = similarity_matrix[0, 1]
            # similarity_score = cosine_sim(main_summary, summary_2)
            similarity_list.append(cosine_similarity_value)
        similarity_compared_to_own_gender[main_summary_name] = sum(similarity_list)/len(similarity_list)
    
    # COMPARE TO THE OTHER GENDER
    for main_summary_name, main_summary in main_corpus.items():
        for summary_2_name, summary_2 in other_corpus.items():
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform([main_summary, summary_2])
            similarity_matrix = cosine_similarity(tfidf_matrix)
            cosine_similarity_value = similarity_matrix[0, 1]
            # similarity_score = cosine_sim(main_summary, summary_2)
            similarity_list_other.append(cosine_similarity_value)
        similarity_compared_to_other_gender[main_summary_name] = sum(similarity_list_other)/len(similarity_list_other)

    # check the difference in similarity between own gender and
    # the other gender
    sum_items = []
    for key, value in similarity_compared_to_own_gender.items():
        compare_value = similarity_compared_to_other_gender[key]

        if value > compare_value:
            sum_items.append(1)
        else:
            sum_items.append(0)
    
    score = 2 * np.sum(sum_items) / N - 1
    
    avg_sim_self = sum(similarity_compared_to_other_gender.values())/len(similarity_compared_to_other_gender)
    avg_sim_other = sum(similarity_compared_to_other_gender.values())/len(similarity_compared_to_other_gender)

    return avg_sim_other, avg_sim_self, score

# def calculate_similarity(corpus):
#     similarity_score = {}
#     vectorizer = CountVectorizer()
#     bow = vectorizer.fit_transform(corpus)
#     for pair in combinations(bow, 2):
        
#         a, b = pair
#         a = a.toarray().squeeze()
#         b = b.toarray().squeeze()
#         # unique_pairs.add(tuple(sorted((a,b))))
#         similarity_score[counter] = cosine_sim(a, b)
#         counter += 1

#     avg_similarity = sum(similarity_score.values())/len(similarity_score)
#     return avg_similarity


def calculate_representation_bias(datasets, gender_str):
    """Calculates representation bias by using the equation
    mentioned in section 4.1.4 of the paper"""
    
    for dataset in datasets:
        folder_path = 'Outputs/' + dataset
        file_pattern = '*.txt'  # Example: List all .txt files

        files = glob.glob(os.path.join(folder_path, file_pattern))
        summaries = {}
        for filename in files:
            with open(filename, "r") as file:
                summary = file.read()
                summaries[filename] = summary
        
        if 'female' in dataset and gender_str == 'f':
            main_summaries = summaries
        elif 'female' in dataset and gender_str == 'm':
            other_summaries = summaries
        elif 'male' in dataset and gender_str == 'f':
            other_summaries = summaries
        elif 'male' in dataset and gender_str == 'm':
            main_summaries = summaries
    
    avg_sim_other, avg_sim_self, score = calculate_similarity(main_summaries, other_summaries)

    print('Gender string: ', gender_str, avg_sim_other, avg_sim_self, score)

    return score

    # if gender_str == 'f':
    #     if similarity[datasets[0]] > similarity[datasets[1]]:
    #         item_to_sum = 1
    #     else:
    #         item_to_sum = 0
    #     representation_bias_score = 2/N * item_to_sum - 1
    
    # if gender_str == 'm':
    #     if similarity[datasets[0]] < similarity[datasets[1]]:
    #         item_to_sum = 1
    #     else:
    #         item_to_sum = 0
    #     representation_bias_score = 2/N * item_to_sum - 1

    # return representation_bias_score



model_name = 'summaries_legal_led'
datasets = [model_name + '_female_only', model_name + '_male_only']

rep_bias_score_f = calculate_representation_bias(datasets, 'f')
rep_bias_score_m = calculate_representation_bias(datasets, 'm')

print("Representation bias for rep_bias_score where we check if female is distingushable from male", rep_bias_score_f)
print("Representation bias for rep_bias_score where we check if male is distingushable from female", rep_bias_score_m)

# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import numpy as np

# def compute_similarity_matrix(corpus):
#     # Use TfidfVectorizer to convert text data to TF-IDF features
#     vectorizer = TfidfVectorizer()
#     tfidf_matrix = vectorizer.fit_transform(corpus)

#     # Compute cosine similarity matrix
#     similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
#     return similarity_matrix

# def distinguishability_score(corpus_female, corpus_male):
#     N = min(len(corpus_female), len(corpus_male))

#     distinguishability_scores = []

#     for i in range(N):
#         # Calculate cosine similarity within the same group
#         s_female = np.mean(compute_similarity_matrix([corpus_female[i]]))
#         s_male = np.mean(compute_similarity_matrix([corpus_male[i]]))

#         # Calculate cosine similarity with the other group
#         other_female = np.mean(compute_similarity_matrix([corpus_male[i]]))
#         other_male = np.mean(compute_similarity_matrix([corpus_female[i]]))

#         # Check distinguishability condition
#         if s_female > other_female and s_male > other_male:
#             distinguishability_scores.append(1)
#         else:
#             distinguishability_scores.append(0)

#     return 2 * np.sum(distinguishability_scores) / N - 1

# model_name = 'summaries_legal_led'
# datasets = [model_name + '_female_only', model_name + '_male_only']
# for dataset in datasets:
#     folder_path = 'Outputs/' + dataset
#     file_pattern = '*.txt'  # Example: List all .txt files

#     files = glob.glob(os.path.join(folder_path, file_pattern))
#     summaries = []
#     for filename in files:
#         with open(filename, "r") as file:
#             summary = file.read()
#             summaries.append(summary)
    
#     if 'female' in dataset:
#         Cmono_female = summaries
#     else:
#         Cmono_male = summaries


# score = distinguishability_score(Cmono_female, Cmono_male)
# print("Distinguishability Score:", score)
