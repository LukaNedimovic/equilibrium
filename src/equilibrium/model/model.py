import numpy as np # Math

from sklearn.metrics.pairwise import cosine_similarity      # Measuring the similarity
from sklearn.feature_extraction.text import TfidfVectorizer # Vectorizing the articles
from sklearn.preprocessing import normalize                 # Normalization
from nltk.corpus import stopwords # Removing stopwords (preprocessing)

from scipy.sparse import csr_matrix # Typehinting

from article.articles import Articles # Articles wrapper

from joblib import dump, load         # Saving data onto the disk


class Model:
    def __init__(self, 
                 path_tfidf_vectorizer:          str, 
                 path_tfidf_matrix:              str, 
                 path_tfidf_cosine_similarities: str):
        """
        Creates an instance of Model used for article recommendations.
        Model is implementing a TF-IDF vectorizer, combined with
        cosine similarity.

        Parameters
        ----------
        path_tfidf_vectorizer : str
            Path to TF-IDF vectorizer.
        path_tfidf_matrix : TYPE
            Path to TF-IDF file.
        path_tfidf_cosine_similarities : TYPE
            Path to cosine similarities file.
        """
        
        self.model_name = "Article TF-IDF MODEL"
    
        # Loading vectorizer
        try:    
            self.vectorizer = load(path_tfidf_vectorizer)    
            self.features =  np.array(self.vectorizer.get_feature_names_out()) 
            
        except Exception as err:
            self.inform(f"[TF-IDF VECTORIZER LOADING ERROR]: {err}")

        # Loading TF-IDF matrix
        try: 
            self.tfidf_matrix = load(path_tfidf_matrix).toarray()
        except Exception as err:
            # Matrix can not be loaded, most likely because it does not exist
            self.inform(f"[TF-IDF MATRIX LOADING ERRROR]: {err}")

        # Loading TF-IDF cosine similarities
        try:
            self.cosine_similarities = load(path_tfidf_cosine_similarities)
        except Exception as err:
            self.inform(f"[TF-IDF COSINE SIMILARITIES LOADING ERROR]: {err}") 
        
        self.num_articles, self.num_features = self.tfidf_matrix.shape

    
    def __str__(self):
        return self.model_name
    
    
    def __getitem__(self, pos: int):
        return self.tfidf_matrix[pos]
    
    
    def __setitem__(self, pos: int, val: csr_matrix): 
        self.tfidf_matrix[pos] = val
        
    
    def recommend(self, article_id: int, quantity: int = 5) -> list:    
        """
        Recommends top-`quantity` articles similar to the article
        with id `article-id`.

        Parameters
        ----------
        article_id : int
            Article whose similar articles are to be found.
        quantity : int, optional
            The number of articles to recommend. The default is 5.

        Returns
        -------
        list
            List of top-`quantity` similar articles.

        """
        
        # Get the indices of the top `quantity` most similar articles 
        # It is also needed to remove the article itself
        most_similar_ids = np.argsort(self.cosine_similarities[article_id])[-quantity-1:-1][::-1]
        
        return most_similar_ids
    
    
    def calculate_similarities_keywords_article(self, keywords: list) -> list:
        """
        Returns
        -------
        list
            List of the most similar articles, given certain keywords. 
            Used for searching.
        """
        keyword_vector = self.vectorizer.transform([' '.join(keywords)])

        # Calculate cosine similarity between the keyword vector and all article vectors
        similarities = cosine_similarity(keyword_vector, self.tfidf_matrix)

        # Extract the similarity scores for each article
        article_similarities = similarities[0]

        # Combine article indices with their similarity scores
        article_scores = list(enumerate(article_similarities))

        # Sort the articles by similarity score in descending order
        sorted_articles = sorted(article_scores, key=lambda x: x[1], reverse=True)

        return sorted_articles
    
    
    def search(self, 
               articles: Articles, 
               keywords: list, 
               quantity: int = 5) -> list:
        """
        Search for top-`quantity` similar articles, given keywords.

        Parameters
        ----------
        articles : Articles
            All articles available on platform, loaded into a wrapper.
        keywords : list
            Keywords entered in search input box.
        quantity : int, optional
            The number of articles to be returned after searching. 
            The default is 5.
            
        Returns
        -------
        list:
            Search result.
        """
        
        similarities = self.calculate_similarities_keywords_article(keywords)

        # Get the top N recommendations
        top_recommendations = similarities[:quantity]

        # Extract the article indices from the recommendations
        recommended_indices = [index for index, _ in top_recommendations]

        # Get the actual articles based on the indices
        recommended_articles = [articles[index] for index in recommended_indices]
            
        return recommended_articles
    
    
    def refit(self, articles: Articles):
        """
        Refits the model by creating a new one and retraining it, 
        given the new articles wrapper.

        Parameters
        ----------
        articles : Articles
            Articles wrapper that has changed and needs to be fed into
            the model, for it to be retrained.
        """
        
        self.create_new_model(articles=articles)
        
    
    def inform(self, text: str):
        """
        Utility function for easier communication.

        Parameters
        ----------
        text : str
            Text to be printed on screen.
        """
        
        print(f"[{self.model_name}]: {text}")
    
    
    def create_new_model(self, articles: Articles):
        """
        Creates a totally new model and saves it onto the disk.

        Parameters
        ----------
        articles : Articles
            Articles wrapper with all necessary data for training.
        """
        
        self.load_data(articles)
        
        self.create_model()
        self.fit()
        self.calculate_similarities()
        
        self.save()
        
        
    def load_data(self, articles: Articles):
        """
        Loads data into the model.
        
        Parameters
        ----------
        articles : Articles
            Articles wrapper with all necessary data for training.
        """
        
        self.article_ids      = articles["id"]
        self.article_titles   = articles["title"]
        self.article_contents = articles["content"]
        
        self.stopwords = stopwords.words("english")
        
        
    def create_model(self):
        """
        Creates a new TF-IDF model, used for article recommendation.
        The model is also used for searching.
        """
        
        # This is something to play with. 1000 works fine in this case.
        self.MAX_FEATURES = 1000
        
        # A new instance of TfidfVectorizer
        self.vectorizer = TfidfVectorizer(analyzer='word',
                                      ngram_range=(1, 2),
                                      min_df=0.003,
                                      max_df=0.5,
                                      max_features=self.MAX_FEATURES,
                                      stop_words=self.stopwords)
        
        
    def fit(self):
        """
        Train the model to fit onto the new data.
        """
        
        title_text_pairs = ((title + "" + content) 
                            for title, content in 
                            zip(self.article_titles, self.article_contents))
        
        self.tfidf_matrix = self.vectorizer.fit_transform(title_text_pairs)
        
        
    def get_top_words(self):
        """
        Returns top words for each article.
        The number of words is discussable, but 5 worked well in this case.
        """
        
        self.tfidf_feature_names = np.array(self.vectorizer.get_feature_names_out())
        self.dense_tfidf_matrix = self.tfidf_matrix.toarray()
        
        # Iterate over each row (article) in the TF-IDF matrix
        for i in range(self.dense_tfidf_matrix.shape[0]):
            # Get the TF-IDF values for the current article
            tfidf_values = self.dense_tfidf_matrix[i]
        
            # Get the indices of the top 5 TF-IDF values
            top_indices = np.argsort(tfidf_values)[-5:][::-1]
        
            # Get the corresponding words from the feature names
            top_words = self.feature_names[top_indices]
        
            # Print the results for the current article
            print(f"Top 5 words for Article {i}: {top_words}")
        
        
    def calculate_similarities(self):
        """
        Calculates cosine similarity on model's tfidf matrix.
        """
        self.normalized_tfidf_matrix = normalize(self.tfidf_matrix, norm='l2', axis=1)
        
        # Compute cosine similarity between articles
        self.cosine_similarities = cosine_similarity(self.normalized_tfidf_matrix)
            
        
    def save(self):
        """
        Saves the model and other relevant data onto disk.
        """
        dump(self.tfidf_matrix, "tfidf_matrix.joblib")
        dump(self.vectorizer, "tfidf_vectorizer.joblib")
        dump(self.cosine_similarities, "tfidf_cosine_similarities.joblib")