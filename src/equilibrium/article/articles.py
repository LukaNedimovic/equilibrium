from article.article import Article
from user.user import User

from utils.data_wrapper import DataWrapper
from utils.parser import parse_csv, write_line_csv

import ast # Literal evaluation

import os

import matplotlib.pyplot as plt
import numpy as np

class Articles:
    def __init__(self, 
                 path_articles_content: str = "", 
                 path_articles_metadata: str = ""):
        self.path_articles_content  = path_articles_content
        self.path_articles_metadata = path_articles_metadata
        
        self.articles = []
        
    
    def __getitem__(self, key):
        if isinstance(key, int):    
            for article in self.articles:
                if article.id == key:
                    return article
            return None
        
        if isinstance(key, str):
            result = []
            for article in self.articles:
                result.append(getattr(article, key))
            
            return result
    
    def __setitem__(self, id: int, new_value: Article):
        self.articles[id] = new_value
       
    def __len__(self):
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
        keywords_cnt = {}
        for article in self.articles:
            for tag in article.tags:
                if tag not in keywords_cnt:
                    keywords_cnt[tag] = 1
                else:
                    keywords_cnt[tag] += 1
                        
        keywords_cnt_sorted = sorted(keywords_cnt.items(), key=lambda x: x[1], reverse=True)[:20]
        tags, values = zip(*keywords_cnt_sorted)
        
        plt.barh(tags, values, color='skyblue')
        
        plt.xlabel('Frequency')
        plt.ylabel('Tags')
        plt.title('Top 20 tags and their frequiencies')
        
        # Create a horizontal bar chart
        plt.barh(tags, values, color='skyblue')

        plt.show()
        
        
    def like(self, article_id: int, user: User) -> bool:
        target_article = self.articles[article_id]
        
        if article_id not in user.articles_liked:
            if article_id in user.articles_disliked:
                user.articles_disliked.remove(article_id)
                target_article.dislikes -= 1
                
            user.articles_liked.append(article_id)
            target_article.likes += 1
            
            return True

        return False
    
    
    def dislike(self, article_id: int, user: User) -> bool:
        target_article = self.articles[article_id]
        
        if article_id not in user.articles_disliked:
            if article_id in user.articles_liked:
                user.articles_liked.remove(article_id)
                target_article.likes -= 1
                
            user.articles_disliked.append(article_id)
            target_article.dislikes += 1
            
            return True
        
        return False
    
    
    def save(self, article_id: int, user: User) -> bool:
        if article_id not in user.articles_saved:
            user.articles_saved.append(article_id)
            return True
        
        return False
    
    
    def add_new_article(self, new_article_data: dict):
        new_article_id = max(self.articles, key=lambda article: article.id).id + 1
        
        new_article = Article(id=new_article_id,
                              title=new_article_data["title"],
                              tags=new_article_data["tags"],
                              likes=0,
                              dislikes=0,
                              views=0,
                              content=new_article_data["content"],
                              formatted=True)
        
        self.articles.append(new_article)
        
        try:
            content_path = self.path_articles_content / f"article_{new_article_id}.txt"
            content_file = open(content_path, "w", encoding="utf8")
            content_file.write(new_article_data["content"])
            
            content_file.close()
            
        except Exception as err:
            print(f"[ARTICLE CONTENT SAVING ERROR] {err}: Could not write down content for newly created file")
        
        
        write_line_csv(self.path_articles_metadata, new_article.to_metadata_row())
    
    
    def remove_article(self, article_id: int):
        found_idx = 0
        for idx, article in enumerate(self.articles):
            if article.id == article_id:
                found_idx = idx
                break
            
        self.articles.pop(found_idx)
        
        self.write_metadata()
        self.destroy_article(article_id)
        
    
    def get_title_text_pairs(self) -> list:
        result = []
        for article in self.articles:
            result.append((article.title, article.content))
        
        
        return result
    
    def write_metadata(self):
        with open(self.path_articles_metadata, "w", encoding="utf8") as metadata_file:
            metadata_file.write("id,author_id,title,tags,likes,dislikes,views,reading_time,formatted\n")
            for article in self.articles:    
                metadata_file.write(article.to_metadata_row())
    
        
    def destroy_article(self, id: int):
        content_path = self.path_articles_content / f"article_{id}.txt"
        
        try:
            # Delete the file
            os.remove(content_path)
            print("Article has been successfully deleted.")
            
        except OSError as err:
            print(f"[DESTROYING ARTICLE ERROR]: {err}")