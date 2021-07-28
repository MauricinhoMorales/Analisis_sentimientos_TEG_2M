from tweets_management import tweets_management
from tweets_ngrams import tweets_ngrams
from tweets_classification import tweets_classification

# Todos los Usuarios entre 19 y 38 años
# users_19_38_all = ['raleonc71','RiccardoLobo','AndresFGuevaraB','clavelrangel','ramses_siverio','ricardolodice','kevinaviladdhh','jhoalys','gabosantana35','orianafaoro','TatoCelis','salvabenasayag','JesusMolinaCs','bpulidom','gzuzkstro','Rogerlruizh9','paola_morales14','Arthur_Canga','YoSoyMarlys','vicman_ve','anthxnyb_','Isaacsb2000','nisequiensoypue','Demenciand0']

# Usuarios entre 19 y 38 años cuyos tweets todavia no estan traducidos 
# users_38_19_missing = ['orianafaoro','TatoCelis','salvabenasayag','gzuzkstro','paola_morales14','YoSoyMarlys','vicman_ve','anthxnyb_','Isaacsb2000','nisequiensoypue']

# Usuarios entre 19 y 38 años cuyos tweets ya están traducidos
users_38_19_translated = ['raleonc71','AndresFGuevaraB','clavelrangel','ricardolodice','kevinaviladdhh','jhoalys','gabosantana35','salvabenasayag','bpulidom','gzuzkstro','Rogerlruizh9','Arthur_Canga']

# Variables para identificar a que carpetas seran guardadas
individual_folders = 'users'
batch_folder = 'batch'

user_twitter = tweets_management('nlluengo',individual_folders)
# user_twitter.scraping(100)
user_twitter.cleaning()
user_twitter.sentiment_analysis()

# for user in users_38_19_translated:
    
#     user_twitter = tweets_management(user,individual_folders)
#     # user_twitter.scraping(1000)
#     # user_twitter.cleaning()
#     user_twitter.sentiment_analysis()
        
#     sorter = tweets_classification(user)
#     sorter.training(0.3)
#     sorter.test_Naive_Bayes()
#     sorter.test_SVM()
#     sorter.test_Decision_Forest()
#     sorter.test_Max_Entropy()
        
#     user_tweets_ngrams = tweets_ngrams(user,individual_folders)
#     # user_tweets_ngrams.monogramming()
#     # user_tweets_ngrams.ngraming()

# user_tweets_ngrams = tweets_ngrams('','')
# # user_tweets_ngrams.ngraming_in_one_file(individual_folders, batch_folder, users_lists_38_19)
