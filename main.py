from tweets_management import tweets_management
from tweets_ngrams import tweets_ngrams
from tweets_classification import tweets_classification

# Todos los Usuarios entre 19 y 38 años
# users_19_38_all = ['raleonc71','RiccardoLobo','AndresFGuevaraB','clavelrangel','ramses_siverio','ricardolodice','kevinaviladdhh','jhoalys','gabosantana35','orianafaoro','TatoCelis','salvabenasayag','JesusMolinaCs','bpulidom','gzuzkstro','Rogerlruizh9','paola_morales14','Arthur_Canga','YoSoyMarlys','vicman_ve','anthxnyb_','Isaacsb2000','nisequiensoypue','Demenciand0']

# Usuarios entre 19 y 38 años cuyos tweets todavia no estan traducidos 
# users_38_19_missing = ['orianafaoro','TatoCelis','salvabenasayag','gzuzkstro','paola_morales14','YoSoyMarlys','vicman_ve','anthxnyb_','Isaacsb2000','nisequiensoypue']

# Usuarios entre 19 y 38 años cuyos tweets ya están traducidos
users_38_19_translated = ['AndresFGuevaraB','Arthur_Canga','bpulidom','clavelrangel','gabosantana35','jhoalys','kevinaviladdhh','raleonc71','ricardolodice','Rogerlruizh9']

# lista de prueba
# list=['Rogerlruizh9']

# Variables para identificar a que carpetas seran guardadas
individual_folders = 'users'
batch_folder = 'batch'

for user in users_38_19_translated:
    
    user_twitter = tweets_management(user,individual_folders)
    # user_twitter.scraping(1000)
    # user_twitter.cleaning()
    # user_twitter.sentiment_analysis()
    # user_twitter.clean_sentiments()

    sorter = tweets_classification(user,individual_folders)
    # sorter.training(0.25)
    # sorter.test_Naive_Bayes()
    # sorter.test_SVM()
    # sorter.test_Decision_Forest()
    # sorter.test_Max_Entropy()
    
    sorter_batch = tweets_classification(user,batch_folder)
    # sorter_batch.load()
        
    user_tweets_ngrams = tweets_ngrams(user,individual_folders)
    # user_tweets_ngrams.monogramming()
    # user_tweets_ngrams.ngraming()

user_tweets_ngrams = tweets_ngrams('',batch_folder)
# user_tweets_ngrams.ngraming_in_one_file(users_lists_38_19)

sorter = tweets_classification('',batch_folder)
# sorter.training(0.25)
# sorter.test_Naive_Bayes()
# sorter.test_SVM()
# sorter.test_Decision_Forest()
# sorter.test_Max_Entropy()