from tweets_management import tweets_management
from tweets_ngrams import tweets_ngrams
from tweets_classification import tweets_classification

folders_users_individuals = 'users_folders'
folder_all_in_one_file = 'user_one_file'

# users_lists_38_19 = ['raleonc71','RiccardoLobo','AndresFGuevaraB','clavelrangel','ramses_siverio','ricardolodice','kevinaviladdhh','jhoalys','gabosantana35','orianafaoro','TatoCelis','salvabenasayag','JesusMolinaCs','bpulidom','gzuzkstro','Rogerlruizh9','paola_morales14','Arthur_Canga','YoSoyMarlys','vicman_ve','anthxnyb_','Isaacsb2000','nisequiensoypue','Demenciand0']
users_lists_38_19 = ['orianafaoro','TatoCelis','salvabenasayag','gzuzkstro','paola_morales14','YoSoyMarlys','vicman_ve','anthxnyb_','Isaacsb2000','nisequiensoypue']

for user in users_lists_38_19:
    # user_twitter = tweets_management(user,folders_users_individuals)
     
    # user_twitter.scraping(1000)
    # user_twitter.cleaning()

    # sorter = classification(user)

    # sorter.training(0.3)
    # sorter.test_naive_bayes()
    # sorter.test_SVM()
    # sorter.test_Decision_Forest()

    # user_tweets_ngrams = tweets_ngrams(user,folders_users_individuals)

    # user_tweets_ngrams.monogramming()
    # user_tweets_ngrams.ngraming()
    pass

user_tweets_ngrams = tweets_ngrams('','')
user_tweets_ngrams.ngraming_in_one_file(folders_users_individuals, folder_all_in_one_file, users_lists_38_19)
