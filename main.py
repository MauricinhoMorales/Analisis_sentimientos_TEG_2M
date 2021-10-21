from tweets_management import tweets_management
from tweets_ngrams import tweets_ngrams
from tweets_classification import tweets_classification

sentimiento_folder = 'sentimiento'
opinion_folder = 'opinion'
mensajes_folder = 'mensajes'

sentimiento = tweets_management(sentimiento_folder)
sentimiento.cleaning()

opinion = tweets_management(opinion_folder)
opinion.cleaning()

sorter_sentimiento = tweets_classification(sentimiento_folder)
sorter_sentimiento.training(0.1,0.9)
sorter_sentimiento.test_Naive_Bayes()
sorter_sentimiento.test_SVM()
sorter_sentimiento.test_Decision_Tree()
sorter_sentimiento.test_Max_Entropy()
sorter_sentimiento.test_batch()

sorter_opinion = tweets_classification(opinion_folder)
sorter_opinion.training(0.1,0.9)
sorter_opinion.test_Naive_Bayes()
sorter_opinion.test_SVM()
sorter_opinion.test_Decision_Tree()
sorter_opinion.test_Max_Entropy()
sorter_opinion.test_batch()

n_grams_sentimiento = tweets_ngrams(sentimiento_folder)
n_grams_sentimiento.monogramming()
n_grams_sentimiento.ngraming()

n_grams_opinion = tweets_ngrams(opinion_folder)
n_grams_opinion.monogramming()
n_grams_opinion.ngraming()