import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process
class moviesuggestion():
    def __init__(self):
        
        self.movie_df=pd.read_csv("Movies_df.csv")
        cid = CountVectorizer(min_df=5,ngram_range=(1,5),stop_words="english")
        cid_matrix_content_based = cid.fit_transform(self.movie_df['content_based'])
        self.cos_similarity_content_based = cosine_similarity(cid_matrix_content_based,cid_matrix_content_based)
        cid = CountVectorizer(max_df=10,ngram_range=(1,2),stop_words="english")
        cid_matrix_keyword_based = cid.fit_transform(self.movie_df['keyword_based'])
        self.cos_similarity_keyword_based = cosine_similarity(cid_matrix_keyword_based,cid_matrix_keyword_based)
        self.indices = pd.Series(self.movie_df.index,index=self.movie_df['title'])
        self.indices.index=self.indices.index.str.lower()
    def get_dataset(self):
        return self.movie_df
    def get_movies_by_content(self,x):
        idx=self.indices[x]
        l=[i[0] for i in sorted(list(enumerate(self.cos_similarity_content_based[idx])),key=lambda x:x[1],reverse=True)]
        return self.movie_df.iloc[l].fillna("")

    def get_similiar_named_movies(self,x):
        l = [i[0] for i in process.extract(x,self.indices.index)]
        return self.movie_df[self.movie_df.title.str.lower().isin(l)].fillna("").drop({"Unnamed: 0"},axis=1)

    def get_movies_by_keywords(self,x):
        idx=self.indices[x]
        l=[i[0] for i in sorted(list(enumerate(self.cos_similarity_keyword_based[idx])),key=lambda x:x[1],reverse=True)]
        return self.movie_df.iloc[l].fillna("")