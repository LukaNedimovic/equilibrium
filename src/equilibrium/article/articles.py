import numpy as np
import matplotlib.pyplot as plt

from utils.data_wrapper import DataWrapper
from utils.parser import parse_csv, write_line_csv
import os 
import ast 

from article.article import Article
from user.user import User

from typing import Tuple

class Articles:
    def __init__(self, 
                 path_articles_content:  str = "", 
                 path_articles_metadata: str = ""):
        """
        Creates an instance of Articles wrapper.
        """
        
        self.path_articles_content  = path_articles_content   # Content folder
        self.path_articles_metadata = path_articles_metadata  # Metadata file
        
        self.articles = [] # List of all articles as objects
        
    
    def __getitem__(self, key):
        # If key is an integer, then retrieve the article with given ID
        if isinstance(key, int):    
            for article in self.articles:
                if article.id == key:
                    return article
            return None # Return `None` if the given ID doesn't exist
        
        # If given a string, return the given property of every single article
        elif isinstance(key, str):
            result = []
            for article in self.articles:
                result.append(getattr(article, key))
            
            return result # Properties concatenated
    
    
    def __setitem__(self, id: int, new_value: Article):
        """
        Sets a new article, given ID
        """
        self.articles[id] = new_value
       
        
    def __len__(self) -> int:
        """
        Returns
        -------
        int
            Total number of articles inside a wrapper.
        """
        return len(self.articles)
       
    
    def __str__(self) -> str:
        all_articles_str = "\n".join(self.articles)
        return all_articles_str
    
    
    def __repr__(self) -> str:
        return f"Articles Wrapper ({len(self.articles)})"
    
    
    def append(self, article: Article):
        """
        Appends an article at the end of the list of articles.
        
        Parameters
        ----------
        article : Article
            New article to be appended to the end of the list.
        """
        
        self.articles.append(article)
        
    
    def load(self):
        """
        Loads articles into wrapper.
        """
        
        print("[Articles Wrapper]: Starting to load articles.")
        articles_metadata_parsed  = parse_csv(self.path_articles_metadata)
        articles_metadata_wrapped = DataWrapper(articles_metadata_parsed) 

        
        articles_num = articles_metadata_wrapped.shape[1]
        
        # For each article
        for id in range(articles_num):
            content = "" # Set the content to empty
            # Try loading the content from separate file
            try:
                content_path = self.path_articles_content / f"article_{id}.txt"
                content = open(content_path, encoding="utf8").read()
                
            except Exception as err:
                # Article's content can not be loaded, 
                # most likely because it does not exist
                print(f"[ARTICLE LOADING ERROR] {err}: Can't find content for article {id}.")
                
                
            (_, 
            author_id, 
            title, 
            tags, 
            likes, 
            dislikes, 
            views, 
            reading_time, 
            formatted) = articles_metadata_wrapped[id].values() # Unpack metadata
            
            # Literally evaluate for the sake of program's logic
            # title = ast.literal_eval(title)
            if title[0] != '"':
                title = '"' + title
            
            if title[-1] != '"':
                title = title + '"'

            # Literally evaluate everything
            author_id = ast.literal_eval(author_id) 
            tags = ast.literal_eval(tags)
            likes = ast.literal_eval(likes)
            dislikes = ast.literal_eval(dislikes)
            views = ast.literal_eval(views)
            reading_time = ast.literal_eval(reading_time)
            formatted = ast.literal_eval(formatted)
            
            new_article = Article(id=id,
                                  title=title,
                                  author_id=author_id,
                                  tags=tags,
                                  content=content,
                                  likes=likes,
                                  dislikes=dislikes,
                                  views=views,
                                  reading_time=reading_time,
                                  formatted=formatted)
            
            self.append(new_article)
            
        print("[Articles Wrapper]: Articles successfully loaded.")


    def show_platform_statistics_interactions(self, num_users: int = 1):
        """
        Shows total platform statistics.
        
        Parameters
        ----------
        num_users : int
            Number of users on the platform. 
            Needs to be passed from User wrapper.
        """
        
        all_likes    = sum([article.likes    for article in self.articles])
        all_dislikes = sum([article.dislikes for article in self.articles])
        all_views    = sum([article.views    for article in self.articles])
        
        fig, ax = plt.subplots(figsize=(8, 5))
        bar_width = 0.5
        bar_positions = np.arange(5)
        
        ax.bar(bar_positions, [len(self.articles), num_users, all_likes, all_dislikes, all_views],
               bar_width,
               color=["skyblue", "skyblue", "skyblue", "skyblue", "skyblue"])

        ax.set_xticks(bar_positions)
        ax.set_xticklabels(["Articles", "Users", "Likes", "Dislikes", "Views"])
        ax.set_ylabel("Count")
        ax.set_title("Complete platform statistics")

        plt.tight_layout()
        plt.show()
        
        
    def show_platform_statistics_tags(self, keywords: list = []):
        """
        Shows tags distribution on platform.
        Only available for Admin account.

        Parameters
        ----------
        keywords : list, optional
            List of keywords (tags).
        """
        
        
        # Counts each keyword present in all the articles
        keywords_cnt = {}
        for article in self.articles:
            for tag in article.tags:
                if tag not in keywords_cnt:
                    keywords_cnt[tag] = 1
                else:
                    keywords_cnt[tag] += 1
                    
        # Sorts the keywords and swaps them
        keywords_cnt_sorted = sorted(keywords_cnt.items(), key=lambda x: x[1], reverse=True)[:20]
        tags, values = zip(*keywords_cnt_sorted)
        
        
        # Plotting part
        plt.barh(tags, values, color='skyblue')
        
        plt.xlabel('Frequency')
        plt.ylabel('Tags')
        plt.title('Top 20 tags and their frequiencies')
        
        # Create a horizontal bar chart
        plt.barh(tags, values, color='skyblue')

        plt.show()
        
        
    def like(self, article_id: int, user: User) -> bool:
        """
        Likes an article, whose ID is `article_id`, by `user`.
        
        Parameters
        ----------
        article_id : int
            ID of an article that is being liked.
        user : User
            User object that is liking the article.
            
            
        Returns
        -------
        bool
            If article is successfully liked - return True and increment
            like count on screen.
            Otherwise, return False (`user` has already liked this article).
        """
        
        target_article = self.articles[article_id] # Get the target article
        
        if article_id not in user.articles_liked:     # If article is not liked
            if article_id in user.articles_disliked:  # Remove from disliked
                user.articles_disliked.remove(article_id)
                target_article.dislikes -= 1
                
            # Like the article
            user.articles_liked.append(article_id) 
            target_article.likes += 1
            
            return True # Article has a new like

        return False # Nothing has changed - article is already liked
    
    
    def dislike(self, article_id: int, user: User) -> bool:
        """
        Dislikes an article, whose ID is `article_id`, by `user`.
        
        Parameters
        ----------
        article_id : int
            ID of an article that is being disliked.
        user : User
            User object that is disliking the article.
            
        Returns
        -------
        bool
            If article is successfully disliked - return True and increment
            dislike count on screen.
            Otherwise, return False (`user` has already liked this article).
        """
        
        target_article = self.articles[article_id] # Get the target article 
        
        if article_id not in user.articles_disliked: # If article is not disliked
            if article_id in user.articles_liked:    # Remove from liked
                user.articles_liked.remove(article_id)
                target_article.likes -= 1
                
            # Dislike the article
            user.articles_disliked.append(article_id)
            target_article.dislikes += 1
            
            return True # Article has a new dislike
        
        return False # Nothing has changed - article is already disliked
    
    
    def save(self, article_id: int, user: User) -> bool:
        """
        Saves an article, whose ID is `article_id`, by `user`.
        
        Parameters
        ----------
        article_id : int
            ID of an article that is being saved.
        user : User
            User object that is saving the article.
            
        Returns
        -------
        bool
            If article is successfully saved - return True
            Otherwise, return False (`user` has already saved this article).
        """
        
        if article_id not in user.articles_saved:
            user.articles_saved.append(article_id) 
            return True
        
        return False
    
    
    def add_new_article(self, new_article_data: dict):
        """
        Creates a new article on platform.
        
        Parameters
        ----------
        new_article_data : dict
            Complete data needed to create a new instance of Article class.
        """
        
        # New article's id is the maximum article's id + 1, 
        # so no two articles can possible have the same id
        new_article_id = max(self.articles, key=lambda article: article.id).id + 1
        
        # Creates a new Article instance
        new_article = Article(id=new_article_id,
                              title=new_article_data["title"],
                              tags=new_article_data["tags"],
                              likes=0,
                              dislikes=0,
                              views=0,
                              content=new_article_data["content"],
                              formatted=True)
        
        # Adds it into the wrapper
        self.articles.append(new_article)
        
        
        # Tries writing the data (should go smoothly)
        try:
            content_path = self.path_articles_content / f"article_{new_article_id}.txt"
            content_file = open(content_path, "w", encoding="utf8")
            content_file.write(new_article_data["content"])
            
            content_file.close()
            
        except Exception as err:
            print(f"[ARTICLE CONTENT SAVING ERROR] {err}: Could not write down content for newly created file")
        
        
        # Writes a line into metadata .csv file about a new article created
        write_line_csv(self.path_articles_metadata, new_article.to_metadata_row())
    
    
    def remove_article(self, article_id: int):
        """
        Given ID, removes the article from the wrapper and all data related to
        it from the storage.
        
        Parameters
        ----------
        article_id : int
            ID of the article to be removed.
        """
        
        found_idx = 0
        for idx, article in enumerate(self.articles):
            if article.id == article_id:
                found_idx = idx # Article has been found on index `idx`
                break
            
        self.articles.pop(found_idx)     # Remove the article from the wrapper
        
        self.write_metadata()            # Rewrite metadata of all articles
        self.destroy_article(article_id) # Clear all article data from storage
        
    
    def get_title_text_pairs(self) -> list[Tuple[str, str]]:
        """
        Returns
        -------
        list
            List of (title, text) pairs for each article in the wrapper.
        """
        
        result = []
        for article in self.articles:
            result.append((article.title, article.content))
        
        
        return result
    
    def write_metadata(self):
        """
        Writes metadata of current article wrapper into desiganted file.
        """
        with open(self.path_articles_metadata, "w", encoding="utf8") as metadata_file:
            metadata_file.write("id,author_id,title,tags,likes,dislikes,views,reading_time,formatted\n")
            for article in self.articles:    
                metadata_file.write(article.to_metadata_row())
    
        
    def destroy_article(self, id: int):
        """
        Deletes the article from storage.
        """
        
        # Path of the article to be deleted
        content_path = self.path_articles_content / f"article_{id}.txt"
        
        try:
            # Delete the file
            os.remove(content_path)
            print("Article has been successfully deleted.")
            
        except OSError as err:
            print(f"[DESTROYING ARTICLE ERROR]: {err}")