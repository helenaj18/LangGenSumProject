from scipy import stats
import math

def calculate_significance(mean_a, mean_b, stdev_a, stdev_b, n_a, n_b, description):
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
        print("P value < " + str(alpha) + " so the difference is significant for " + description)
    else:
        significant = False
        print("P value < " + str(alpha) + " so the difference is NOT significant for " + description)
    
    return significant


# Significance within the same model
calculate_significance(0.16970443349753692, 0.39950934396747245, 0.24337270850338416, 0.1907044302057675, 203, 203, "Female vs male words ratio LED-base") 
calculate_significance(0.007518796992481203, 0.003977204917054541, 0.086710996952412, 0.019433533971473044, 133, 133, "Female vs male names ratio LED-base") 
calculate_significance(26.914823532104492, 25.005187451839447, 0, 17.761375141884294, 1, 8, "PPL for summaries containing f-names vs m-names LED-base") 
calculate_significance(27.29, 28.75, 13.292945855379738, 17.58069526956938, 77, 201, "PPL for summaries containing f-words vs m-words LED-base") 
calculate_significance(0.08288919138413497,0.05979641440220495,0.08911792240691, 0.08003304757386623,77,201, "Sentiment for summaries containing f-words vs m-words LED-base") 
calculate_significance(0.14722222222222223, 0.027868851870982543,0,0.0717906822999135,1,8, "Sentiment for summaries containing f-names vs m-names LED-base") 


calculate_significance(0.39117992024395937, 0.5364180154820541, 0.22640949878858166, 0.1760282334360659, 203, 203, "Female vs male words ratio LED-legal") 
calculate_significance(0.11340852130325815, 0.26104506011510364, 0.25609948685207184, 0.34351619335221917, 203, 203, "Female vs male names ratio LED-legal") 
calculate_significance(6.793477831215694, 6.672778910539281, 1.461530197886022, 1.6213202663435466, 203, 203, "PPL for summaries containing f-names vs m-names LED-legal") 
calculate_significance(6.3756461090215755, 6.349979711870842, 2.2245759813854082, 2.3402133163651904, 203, 203, "PPL for summaries containing f-words vs m-words LED-legal") 
calculate_significance(-0.051100472492422805, -0.04027779421304281,0.0866385701656323, 0.09253759930473679, 179, 203, "Sentiment for summaries containing f-words vs m-words LED-legal") 
calculate_significance(-0.042667551168127635, -0.05924116905101729,0.0925449390563516, 0.08031424835854091, 29, 137,  "Sentiment for summaries containing f-names vs m-names LED-legal") 

calculate_significance(0.1515247478301665, 0.4431777308624602,0.2485200548070268, 0.16933042818077,203,203, "Female vs male words ratio Long T5") 
calculate_significance(0.0, 0.0028548936443673284, 0.0, 0.014933128126107337,133,133, "Female vs male names ratio Long T5") 
calculate_significance(37.807292395371654, 31.21707774624966,21.198715805860125, 19.036345055654884,65,202,  "PPL for summaries containing f-words vs m-words Long T5") 
# calculate_significance(None, 27.15965042114258,0, 2.3402133163651904,x,y, "PPL for summaries containing f-names vs m-names Long T5") 
calculate_significance(0.12908725697755366, 0.11220082944602364,0.09797319626692085, 0.11444393749126687,65,203, "Sentiment for summaries containing f-words vs m-words Long T5") 
# calculate_significance(x,y,x,y,x,y, "Sentiment for summaries containing f-names vs m-names Long T5") 



# Comparison between models
calculate_significance(0.16970443349753692, 0.39117992024395937, 0.24337270850338416, 0.22640949878858166, 203, 203, "Female words ratio LED-base vs LED-legal") 
calculate_significance(0.39950934396747245, 0.5364180154820541, 0.1907044302057675, 0.1760282334360659, 203, 203,  "Male words ratio LED-base vs LED-legal") 

calculate_significance(0.007518796992481203, 0.11340852130325815, 0.086710996952412, 0.25609948685207184, 133, 133, "Female names ratio LED-base vs LED-legal") 
calculate_significance(0.003977204917054541, 0.26104506011510364, 0.019433533971473044, 0.34351619335221917, 133, 133, "Male names ratio LED-base vs LED-legal") 

# calculate_significance(28.9, 6.35, "Average PPL LED-base vs LED-legal") 
# calculate_significance(0.0589, -0.04, "Avg. TextBlob score LED-base vs LED-legal") 

calculate_significance(27.294949847382384, 6.3756461090215755, 13.292945855379738, 2.2245759813854082,77 ,179, "PPL for summaries containing f-words LED-base vs LED-legal") 
calculate_significance(28.75459781570814, 6.349979711870842,17.58069526956938,2.3402133163651904,201 , 203,"PPL for summaries containing m-words LED-base vs LED-legal") 

calculate_significance(26.914823532104492, 6.793477831215694, 0, 1.461530197886022, 1, 29, "PPL for summaries containing f-names LED-base vs LED-legal") 
calculate_significance(25.005187451839447, 6.672778910539281,17.761375141884294,1.6213202663435466, 8, 127 ,"PPL for summaries containing m-names LED-base vs LED-legal") 

calculate_significance(-0.042667551168127635,0.14722222222222223,0.0925449390563516,0,29,1, "TextBlob for summaries containing f-names LED-base vs LED-legal") 
calculate_significance(-0.05924116905101729,0.027868851870982543,0.08031424835854091,0.0717906822999135,127,8, "TextBlob for summaries containing m-names LED-base vs LED-legal") 

calculate_significance(0.08288919138413497, -0.051100472492422805,0.08911792240691,0.0866385701656323,77,179, "TextBlob for summaries containing f-words LED-base vs LED-legal") 
calculate_significance(0.05979641440220495, -0.04027779421304281, 0.08003304757386623,0.09253759930473679,201,203,"TextBlob for summaries containing m-words LED-base vs LED-legal") 