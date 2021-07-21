import pandas as pd
from IPython.core.display import display

folders_users_individuals = 'users_folders'
folder_all_in_one_file = 'user_one_file'

users_lists_38_19 = ['raleonc71','AndresFGuevaraB','clavelrangel','ramses_siverio','ricardolodice','kevinaviladdhh','jhoalys','gabosantana35','orianafaoro','TatoCelis','salvabenasayag','JesusMolinaCs','bpulidom','gzuzkstro','Rogerlruizh9','paola_morales14','Arthur_Canga','YoSoyMarlys','vicman_ve','anthxnyb_','Isaacsb2000','nisequiensoypue','Demenciand0']

concat_df = pd.DataFrame()

for user in users_lists_38_19:
    df = pd.read_csv("{}//{}//Bigrams_Trigrams.csv".format(folders_users_individuals,user+'_Folder',index=False))
    
    concat_df = concat_df.append(df)

# result = pd.concat(concat_df)
concat_df = concat_df.sort_values(by=['frequency'], ascending=False)
concat_df = concat_df.rename(columns={'bigram/trigram':'bigram_trigram'})

# display(concat_df)

# display(concat_df.bigram_trigram.duplicated())

# display(concat_df.loc[concat_df.bigram_trigram.duplicated(), :])

concat_df_2 = concat_df.groupby('bigram_trigram').agg({'frequency': sum}).reset_index()
concat_df_2 = concat_df_2.sort_values(by=['frequency'], ascending=False)

# display(concat_df_2.head(5))

concat_df_2.to_csv('{}//Bigrams_Trigrams2.csv'.format(folder_all_in_one_file),index=False)