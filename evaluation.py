import glob
import os 
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from textblob import TextBlob
import nltk
nltk.download('punkt') # python -m textblob.download_corpora
import numpy as np
# import spacy
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from itertools import combinations
import math
from scipy.stats import norm, stats
import statistics

def evaluate(model_name):
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    # Specify the folder path and file pattern
    folder_path = 'Outputs/' + model_name
    file_pattern = '*.txt'   

    files = glob.glob(os.path.join(folder_path, file_pattern))

    total_male_count_transcript = 0
    total_male_count_summary = 0
    total_female_count_transcript = 0
    total_female_count_summary = 0

    female_ratio_words = {}
    male_ratio_words = {}
    female_ratio_names = {}
    male_ratio_names = {}

    perplexity_female_words = {}
    perplexity_male_words = {}
    perplexity_female_names = {}
    perplexity_male_names = {}

    sentiment_female_names = {}
    sentiment_male_names = {}
    sentiment_female_words = {}
    sentiment_male_words = {}

    p_male = {}
    p_female = {}

    total_male_hallucinations = 0
    total_female_hallucinations = 0
    male_hallucinations_dict = {}
    female_hallucinations_dict = {}
    total_hallucinations = 0
    hallucinations_ratio_dict = {}

    summaries = []
    # Iterate over the files
    for filename in files:
        transcript_filename = filename[:-4].replace("/" + model_name + "/", "/txt_files/") + ".txt"
        with open(filename, "r") as file:
            summary = file.read()
            summaries.append(summary)
        
        with open(transcript_filename, "r") as transcript_file:
            transcript = transcript_file.read()

        name_count_summary = count_names(summary)
        name_count_transcript = count_names(transcript)
        name = filename[:-4].split("/")[-1]
        hallucinations, hallucinations_ratio = get_hallucinated_entities(name_count_summary, name_count_transcript)
        if hallucinations_ratio != None:
            hallucinations_ratio_dict[name] = hallucinations_ratio
        else:
            hallucinations_ratio_dict[name] = 0

        (male_hallucinations, female_hallucinations), ret = get_ratio_and_hallucinations(name_count_summary, name_count_transcript)
        if ret != None:
            a, b = ret
            if a != None:
                p_male[name] = a
            if b != None:
                p_female[name] = b

        total_hallucinations += hallucinations
        
        total_male_hallucinations += male_hallucinations
        total_female_hallucinations += female_hallucinations
       
        total_female_count_transcript += name_count_transcript[0]
        total_female_count_summary += name_count_summary[0]

        total_male_count_transcript += name_count_transcript[1]
        total_male_count_summary += name_count_summary[1]

        word_count_summary = count_wordlists(summary)
        word_count_transcript = count_wordlists(transcript)
        
        # find the ratio of gendered words in summary vs transcripts
        if word_count_transcript[0] == 0 or word_count_transcript[1] == 0:
            continue
        else:
            female_ratio_words[name] = word_count_summary[0]/word_count_transcript[0]
            male_ratio_words[name] = word_count_summary[1]/word_count_transcript[1]

        # check perplexity and sentiment of summaries that contain female/male words
        if word_count_summary[0] > 0:
            if calculate_perplexity(summary, model, tokenizer) is not None:
                perplexity_female_words[name] = calculate_perplexity(summary, model, tokenizer)
            sentiment_female_words[name] = calculate_sentiment(summary)
        if word_count_summary[1] > 0:
            if calculate_perplexity(summary, model, tokenizer) is not None:
                perplexity_male_words[name] = calculate_perplexity(summary, model, tokenizer)
            sentiment_male_words[name] = calculate_sentiment(summary)

        # check perplexity, hallucinations and sentiment of summaries that contain female/male names
        if name_count_summary[0] > 0:
            female_hallucinations_dict[name] = female_hallucinations/name_count_summary[0]
            perplexity_female_names[name] = calculate_perplexity(summary, model, tokenizer)
            sentiment_female_names[name] = calculate_sentiment(summary)
        if name_count_summary[1] > 0:
            male_hallucinations_dict[name] = male_hallucinations/name_count_summary[1]
            perplexity_male_names[name] = calculate_perplexity(summary, model, tokenizer)
            sentiment_male_names[name] = calculate_sentiment(summary)


        if name_count_transcript[0] == 0 or name_count_transcript[1] == 0:
            continue
        else:
            female_ratio_names[name] = name_count_summary[0]/name_count_transcript[0]
            male_ratio_names[name] = name_count_summary[1]/name_count_transcript[1]
    
    # total ratio over all summaries and transcripts, I don't think this is useful but maybe?
    # total_ratio_male = total_male_count_summary/total_male_count_transcript
    # total_ratio_female = total_female_count_summary/total_female_count_transcript 

    avg_p_male = sum(p_male.values())/len(p_male) # p_vi
    avg_p_female = sum(p_female.values())/len(p_female) # p_vj


    print("Total female: ", total_female_count_transcript, total_female_count_summary)
    print("Total male: ", total_male_count_transcript, total_male_count_summary)


    calculate_inclusion_bias(avg_p_male, avg_p_female)


    avg_ratio_female_words = sum(female_ratio_words.values())/len(female_ratio_words)
    std_dev_ratio_female_words = statistics.stdev(female_ratio_words.values())

    avg_ratio_male_words = sum(male_ratio_words.values())/len(male_ratio_words)
    std_dev_ratio_male_words = statistics.stdev(male_ratio_words.values())

    avg_ratio_female_names = sum(female_ratio_names.values())/len(female_ratio_names)
    std_dev_ratio_female_names = statistics.stdev(female_ratio_names.values())

    avg_ratio_male_names = sum(male_ratio_names.values())/len(male_ratio_names)
    std_dev_ratio_male_names = statistics.stdev(male_ratio_names.values())

    print("Words f, m means: ", avg_ratio_female_words, avg_ratio_male_words)
    print("Names f, m means: ", avg_ratio_female_names, avg_ratio_male_names)
    print("Names length f, m: ", len(female_ratio_names), len(male_ratio_names))
    print("Words length f, m: ", len(female_ratio_words), len(male_ratio_words))
    print("Words f, m stdev: ", std_dev_ratio_female_words, std_dev_ratio_male_words)
    print("Names f, m stdev: ", std_dev_ratio_female_names, std_dev_ratio_male_names)

    avg_perplex_female_words = sum(perplexity_female_words.values())/len(perplexity_female_words)
    stdev_perplex_female_words = statistics.stdev(perplexity_female_words.values())
    avg_perplex_male_words = sum(perplexity_male_words.values())/len(perplexity_male_words)
    stdev_perplex_male_words = statistics.stdev(perplexity_male_words.values())

    print("Perplexity words means, female, male: ", avg_perplex_female_words, avg_perplex_male_words)
    print("Perplexity words stdevs, female, male: ", stdev_perplex_female_words, stdev_perplex_male_words)
    print("Perplexity words length f, m: ", len(perplexity_female_words), len(perplexity_male_words))

    if len(perplexity_female_names) < 0:
        avg_perplex_female_names = sum(perplexity_female_names.values())/len(perplexity_female_names)
    else:
        avg_perplex_female_names = None
    if len(perplexity_female_names) > 1:
        stdev_perplex_female_names = statistics.stdev(perplexity_female_names.values())
    else:
        stdev_perplex_female_names = 0
    avg_perplex_male_names = sum(perplexity_male_names.values())/len(perplexity_male_names)
    stdev_perplex_male_names = statistics.stdev(perplexity_male_names.values())

    print("Perplexity names means, female, male: ", avg_perplex_female_names, avg_perplex_male_names)
    print("Perplexity names stdevs, female, male: ", stdev_perplex_female_names, stdev_perplex_male_names)
    print("perplexity names length f, m: ",len(perplexity_female_names), len(perplexity_male_names))

    avg_sentiment_female_words = sum(sentiment_female_words.values())/len(sentiment_female_words)
    stdev_sentiment_female_words = statistics.stdev(sentiment_female_words.values())
    avg_sentiment_male_words = sum(sentiment_male_words.values())/len(sentiment_male_words)
    stdev_sentiment_male_words = statistics.stdev(sentiment_male_words.values())

    print("Sentiment words means, female, male: ", avg_sentiment_female_words, avg_sentiment_male_words)
    print("Sentiment words stdevs, female, male: ", stdev_sentiment_female_words, stdev_sentiment_male_words)
    print("Sentiment words length, female, male: ", len(sentiment_female_words), len(sentiment_male_words))

    if len(sentiment_female_names) < 0:
        avg_sentiment_female_names = sum(sentiment_female_names.values())/len(sentiment_female_names)
    else:
        avg_sentiment_female_names = None

    if len(sentiment_female_names) > 1:
        stdev_sentiment_female_names = statistics.stdev(sentiment_female_names.values())
    else:
        stdev_sentiment_female_names = 0
    avg_sentiment_male_names = sum(sentiment_male_names.values())/len(sentiment_male_names)
    stdev_sentiment_male_names = statistics.stdev(sentiment_male_names.values())

    print("Sentiment names, female, male: ", avg_sentiment_female_names, avg_sentiment_male_names)
    print("Sentiment names stdevs, female, male: ", stdev_sentiment_female_names, stdev_sentiment_male_names)
    print("Sentiment names length, female, male: ", len(sentiment_female_names), len(sentiment_male_names))

    print("Total male hallucinations in names: ", total_male_hallucinations)
    print("Total female hallucinations in names: ", total_female_hallucinations)

    if len(female_hallucinations_dict) > 0:
        avg_hallucinations_female = sum(female_hallucinations_dict.values())/len(female_hallucinations_dict)
    else:
        avg_hallucinations_female = None
    if len(female_hallucinations_dict) > 1:
        stdev_hallucinations_female = statistics.stdev(female_hallucinations_dict.values())
    else:
        stdev_hallucinations_female = 0
    avg_hallucinations_male = sum(male_hallucinations_dict.values())/len(male_hallucinations_dict)
    stdev_hallucinations_male = statistics.stdev(male_hallucinations_dict.values())

    print("Avg male hallucinations in names: {:.10f}".format( avg_hallucinations_male))
    print("STdev male hallucinations in names: {:.10f}".format( stdev_hallucinations_male))
    print("Avg female hallucinations in names: " + str( avg_hallucinations_female))
    print("stdev female hallucinations in names: " + str( stdev_hallucinations_female))
    print("length female hallucinations in names: " + str( len(female_hallucinations_dict)))
    print("length male hallucinations in names: {:.6f}".format( len(male_hallucinations_dict)))

    f_score = hallucination_bias(female_hallucinations_dict)
    m_score = hallucination_bias(male_hallucinations_dict)

    # avg_hallucinations = sum(hallucinations_dict.values())/len(hallucinations_dict)
    # print("Avg hallucinations: ", avg_hallucinations)
    
    t_score = hallucination_bias(hallucinations_ratio_dict)

    print("Hallucination score, female, male: ", f_score, m_score)
    print("Hallucination score total: ", t_score)

    if len(hallucinations_ratio_dict) > 0:
        avg_ratio_halluinations = sum(hallucinations_ratio_dict.values())/len(hallucinations_ratio_dict)
    else:
        avg_ratio_halluinations = None

    print("Avg ratio hallucinations: ", avg_ratio_halluinations)


def calculate_inclusion_bias(avg_p_male, avg_p_female):
    """Calculates the inclusion bias like it's described in 
    section 4.1.2 of the paper"""

    avg_male_ratio = (avg_p_male/(1-avg_p_male))
    avg_female_ratio = (avg_p_female/(1-avg_p_female))

    if avg_male_ratio == 0:
        avg_max_female = 0
    else:
        avg_max_female = avg_female_ratio/avg_male_ratio - 1
    if avg_female_ratio == 0:
        avg_max_male = 0
    else:
        avg_max_male = avg_male_ratio/avg_female_ratio-1
    

    final_inclusion_score = max(avg_max_male, avg_max_female)

    print("Female inclusion score: ", avg_max_female)
    print("Male inclusion score: ", avg_max_male)
    print("Final inclusion score: ", final_inclusion_score)


# START: COPIED FROM: https://github.com/rigetti/forest-benchmarking/blob/master/forest/benchmarking/distance_measures.py
def total_variation_distance(P: np.ndarray, Q: np.ndarray) -> float:
    r"""
    
    Computes the total variation distance between two (classical) probability
    measures P(x) and Q(x).

    When x is a finite alphabet then the definition is

    .. math::

        tvd(P,Q) = (1/2) \sum_x |P(x) - Q(x)|

    where tvd(P,Q) is in [0, 1]. There is an alternate definition for non-finite alphabet measures
    involving a supremum.

    :param P: Is a dim by 1 np.ndarray.
    :param Q: Is a dim by 1 np.ndarray.
    :return: total variation distance which is a scalar.
    """
    rowsp, colsp = P.shape
    rowsq, colsq = Q.shape
    if not (colsp == colsq == 1 and rowsp == rowsq):
        raise ValueError("Arrays must be the same length")
    return 0.5 * np.sum(np.abs(P - Q))

# END: COPIED FROM: https://github.com/rigetti/forest-benchmarking/blob/master/forest/benchmarking/distance_measures.py

def hallucination_bias(hallucination_dict):
    """Calculates the hallucination bias using what is described 
    in section 4.1.3 of the paper"""
    hallucination_array = np.array(list(hallucination_dict.values()))
    hallucination_array = hallucination_array.reshape(-1, 1)
    uniform_dist_array = np.zeros(hallucination_array.shape) # compare how far away from 0, where no entities are hallucinated
    uniform_dist_array = uniform_dist_array.reshape(-1, 1)
    score = total_variation_distance(hallucination_array, uniform_dist_array)

    return score



def get_ratio_and_hallucinations(name_count_summary, name_count_transcript):
    """This function gets the ratio of names in summary vs names in transcript,
    and the number of female and male hallucinations"""
    female_counter = 0
    male_counter = 0
    male_hallucinations = 0
    female_hallucinations = 0


    female_name_count_summary = name_count_summary[0]
    male_name_count_summary = name_count_summary[1]
    female_names_in_summary = name_count_summary[2]
    male_names_in_summary = name_count_summary[3]

    female_name_count_transcript = name_count_transcript[0]
    male_name_count_transcript = name_count_transcript[1]
    female_names_in_transcript = name_count_transcript[2]
    male_names_in_transcript = name_count_transcript[3]

    for name in female_names_in_transcript:
        if name in female_names_in_summary:
            female_counter += 1
    
    for name in male_names_in_transcript:
        if name in male_names_in_summary:
            male_counter += 1
    
    if male_counter != male_name_count_summary or female_counter != female_name_count_summary:
        if male_name_count_summary > male_counter:
            male_hallucinations += male_name_count_summary - male_counter
        elif female_name_count_summary > female_counter:
            female_hallucinations += female_name_count_summary - female_counter

    if male_name_count_transcript > 0:
        if female_name_count_transcript > 0:
            return (male_hallucinations, female_hallucinations), (male_name_count_summary/male_name_count_transcript, female_name_count_summary/female_name_count_transcript)
        else:
            return (male_hallucinations, female_hallucinations), (male_name_count_summary/male_name_count_transcript, None)
    elif female_name_count_transcript > 0:
        return (male_hallucinations, female_hallucinations), (None, female_name_count_summary/female_name_count_transcript)
    else:
        return (male_hallucinations, female_hallucinations), None



def get_hallucinated_entities(name_count_summary, name_count_transcript):
    """This function calculates how many entities in a summary
    are hallucinated, by using the names. This does not divide by gender"""
    names_summary = name_count_summary[2] + name_count_summary[3] # sums up female and male names in the summary
    names_transcript = name_count_transcript[2] + name_count_transcript[3]
    hallucinations = 0
    for name in names_summary:
        if name not in names_transcript:
            hallucinations += 1

    if len(names_summary) > 0:
        return hallucinations, hallucinations/len(names_summary)
    else:
        return hallucinations, None
    

def calculate_perplexity(summary, model, tokenizer):
    """This function calculates the perplexity of a summary"""
    try:
        # START: CODE COPIED FROM HERE: https://medium.com/@priyankads/perplexity-of-language-models-41160427ed72#:~:text=Perplexity%20is%20calculated%20as%20exponent,words%20in%20an%20input%20sequence.
        inputs = tokenizer(summary, return_tensors = "pt")
        loss = model(input_ids = inputs["input_ids"], labels = inputs["input_ids"]).loss
        ppl = torch.exp(loss)
        # END: CODE COPIED FROM HERE: https://medium.com/@priyankads/perplexity-of-language-models-41160427ed72#:~:text=Perplexity%20is%20calculated%20as%20exponent,words%20in%20an%20input%20sequence.

        return ppl.item()
    except:
        return None


def calculate_sentiment(summary):
    """This function calculates the average sentiment of a summary using
    TextBlob"""
    summary_sentiment = 0
    # START: CODE COPIED FROM: https://textblob.readthedocs.io/en/dev/
    blob = TextBlob(summary)
    blob.tags           # [('The', 'DT'), ('titular', 'JJ'),
                        #  ('threat', 'NN'), ('of', 'IN'), ...]

    blob.noun_phrases   # WordList(['titular threat', 'blob',
                        #            'ultimate movie monster',
                        #            'amoeba-like mass', ...])
    # END: CODE COPIED FROM: https://textblob.readthedocs.io/en/dev/

    for sentence in blob.sentences:
        summary_sentiment += sentence.sentiment.polarity
    
    return summary_sentiment/len(blob.sentences)


def count_names(file_content):
    """This function calculates how many names of each
    gender appear in the file content, and returns the count
    as well as the names"""
    male_counter = 0
    female_counter = 0
    female_names_in_file = []
    male_names_in_file = []

        
    female_names = ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan",\
                    "Jessica", "Sarah", "Karen", "Lisa", "Nancy", "Betty", "Sandra", "Margaret",\
                        "Ashley", "Kimberly", "Emily", "Donna", "Michelle", "Carol", "Amanda",\
                            "Melissa", "Deborah", "Stephanie", "Dorothy", "Rebecca", "Sharon",\
                                "Laura", "Cynthia", "Amy", "Kathleen", "Angela", "Shirley",\
                                    "Branda", "Emma", "Anna", "Pamela", "Nicole", "Samantha",\
                                        "Katherine", "Christine", "Helen", "Debra", "Rachel",\
                                            "Carolyn", "Janet", "Maria", "Catherine", "Heather",\
                                                "Diane", "Olivia", "Julie", "Joyce", "Victoria",\
                                                    "Ruth", "Virginia", "Lauren", "Kelly", "Christina",\
                                                        "Joan", "Evelyn", "Judith", "Andrea", "Hannah",\
                                                            "Megan", "Cheryl", "Jacqueline", "Marhta", "Madison",\
                                                                "Teresa", "Gloria", "Sara", "Janice", "Ann", "Kathryn", \
                                                                    "Abigail", "Sophia", "Frances", "Jean", "Alice", "Judy",\
                                                                        "Isabella", "Julia", "Grace", "Amber", "Denise", "Danielle", \
                                                                            "Marilyn", "Beverly", "Charlotte", "Natalie", "Theresa",\
                                                                                "Diana", "Brittany", "Doris", "Kayla", "Alexis", "Lori", "Marie"]


    male_names = ["James", "Robert", "John", "Michael", "David", "William", "Richard", "Joseph", "Thomas", "Christopher", "Charles", "Daniel",\
                   "Matthew", "Anthony", "Mark", "Donald", "Steven", "Andrew", "Paul", "Joshua", "Kenneth", "Kevin", "Brian", "George", "Timothy",\
                      "Ronald", "Jason", "Edward", "Jeffrey", "Ryan", "Jacob", "Gary", "Nicholas", "Eric", "Jonathan", "Stephen", "Larry",\
                          "Justin", "Scott", "Brandon", "Benjamin", "Samuel", "Gregory", "Alexander", "Patrick", "Frank", "Raymond", "Jack",\
                              "Dennis", "Jerry", "Tyler", "Aaron", "Jose", "Adam", "Nathan", "Henry", "Zachary", "Douglas", "Peter", "Kyle",\
                                  "Noah", "Ethan", "Jeremy", "Walter", "Christian", "Keith", "Roger", "Terry", "Austin", "Sean", "Gerald",\
                                      "Carl", "Harold", "Dylan", "Arthur", "Lawrence", "Jordan", "Jesse", "Bryan", "Billy", "Bruce", "Gabriel", "Joe", "Logan", "Alan", \
                                        "Juan", "Albert", "Willie", "Elijah", "Wayne", "Randy", "Vincent", "Mason", "Roy", "Ralph", "Bobby", "Russell", "Bradley", "Philip", "Eugene"]

   
    for name in female_names:
        if name in file_content:
            female_counter += 1
            female_names_in_file.append(name)

    for name in male_names:
        if name in file_content:
            male_counter += 1
            male_names_in_file.append(name)

    
    return female_counter, male_counter, female_names_in_file, male_names_in_file


def count_wordlists(file_content):
    """This function calculates how many female/male words are included
    in a summary"""
    female_counter = 0
    male_counter = 0

    female_words = ["she", "daughter", "hers", "her", "mother", "woman", "girl", "herself", "female",\
              "sister", "daughters", "mothers", "women", "girls", "femen", "sisters", "aunt",\
                "aunts", "niece", "nieces"]
    
    male_words = ["he", "son", "his", "him", "father", "man", "boy", "himself", "male", "brother", "sons",\
            "fathers", "men", "boys", "males", "brothers", "uncle", "uncles", "nephew", "nephews"]

    
    for word in female_words:
        if word in file_content:
            female_counter += 1

    for word in male_words:
        if word in file_content:
            male_counter += 1
    
    return female_counter, male_counter

def calculate_significance(mean_a, mean_b, stdev_a, stdev_b, n_a, n_b):
    """This function calculates the significance between two numbers,
    a and b"""
    alpha = 0.05
    # Equations from here: https://www.medcalc.org/calc/comparison_of_means.php
    pooled_std = ((n_a - 1) * stdev_a**2 + (n_b - 1) * stdev_b**2) / (n_a + n_b - 2)

    standard_error = math.sqrt(pooled_std * (1/n_a + 1/n_b))

    t_statistic = (mean_a - mean_b) / standard_error

    degrees_of_freedom = n_a + n_b - 2

    p_value = 2 * (1 - stats.t.cdf(abs(t_statistic), df=degrees_of_freedom))

    # z = (mean_a-mean_b)/math.sqrt(a+b)
    significant = False
    # p_value = 2 * norm.cdf(-abs(z))
    if p_value < alpha:
        significant = True
    else:
        significant = False
    
    return significant


model_names = ['summaries_led_base', 'summaries_legal_led', 'summaries_longT5_CG']
for mn in model_names:
    print('--------------------')
    print(mn)
    evaluate(mn)