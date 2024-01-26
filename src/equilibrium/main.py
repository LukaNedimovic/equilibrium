import time

import numpy as np  

from utils.keypress_detector import capture_keypress, exit
from utils.formatting import clear_screen

from prompt.main_prompt import MainPrompt
from prompt.login_prompt import LoginPrompt
from prompt.user_profile_prompt import UserProfilePrompt
from prompt.add_new_article_prompt import AddNewArticlePrompt
from prompt.search_prompt import SearchPrompt

from user.users import Users

from article.articles import Articles
from article.article_listing import ArticleListing

from model.model import Model

import os
from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

PATH_USERS_DATA     = os.getenv("PATH_USERS_DATA")
PATH_USERS_DATA_CSV = os.getenv("PATH_USERS_DATA_CSV")
def load_users():
    """
    Parses user data from files and loads it into the Users wrapper instance.
    """
    global users 
    users = Users(path_users_data=PROJECT_ROOT / PATH_USERS_DATA_CSV)
    users.load()

    global session
    session = None # In the beggining, there is no active session (User)

    global USER_PROFILE_RESPONSES
    USER_PROFILE_RESPONSES = ["Add New Article",
                              "Search Articles",
                              "My Articles",
                              "Saved Articles",
                              "Platform Statistics (Interactions)",
                              "Platform Statistics (Tags)",
                              "Exit"]

PATH_ARTICLES_CONTENT  = os.getenv("PATH_ARTICLES_CONTENT")
PATH_ARTICLES_METADATA = os.getenv("PATH_ARTICLES_METADATA")
def load_articles():
    """
    Parses article data from files and loads it into the Articles wrapper instance.
    """
    
    global articles
    articles = Articles(path_articles_content=PROJECT_ROOT / PATH_ARTICLES_CONTENT,
                        path_articles_metadata=PROJECT_ROOT / PATH_ARTICLES_METADATA)
    
    articles.load()
    
    global ARTICLE_RESPONSES
    ARTICLE_RESPONSES = ["like", 
                         "dislike", 
                         "recommend", 
                         "comment", 
                         "save"]


PATH_TFIDF_VECTORIZER          = os.getenv("PATH_TFIDF_VECTORIZER")
PATH_TFIDF_MATRIX              = os.getenv("PATH_TFIDF_MATRIX")
PATH_TFIDF_COSINE_SIMILARITIES = os.getenv("PATH_TFIDF_COSINE_SIMILARITIES")
def load_model():
    """
    Loads TF-IDF model that is used for recommending similar articles.
    """
    global model
    model = Model(path_tfidf_vectorizer=PROJECT_ROOT / PATH_TFIDF_VECTORIZER,
                  path_tfidf_matrix=PROJECT_ROOT / PATH_TFIDF_MATRIX,
                  path_tfidf_cosine_similarities=PROJECT_ROOT / PATH_TFIDF_COSINE_SIMILARITIES)


def setup():
    """
    Collection of all other auxiliary functions to be ran.
    """
    load_users()    # Load users into an "Users" wrapper
    load_articles() # Load articles into an "Articles" wrapper
    load_model()    # Load TF-IDF model, used for recommendation

     
def main():
    global session
    global USER_PROFILE_RESPONSES, USER_PROFILE
    global ARTICLE_RESPONSES
    
    current_prompt = MainPrompt("main") # Program starts with the "main" prompt
    
    # model.refit(articles)
    
    while True: 
        time.sleep(0.00000001) # Refresh rate is set to THIS of a second
        clear_screen()        
        current_prompt.show() 

        key = capture_keypress()
        if key is not None:
            response = current_prompt.parse_keypress(key)
            

            # Flexibility - in case there needs to be some other type returned
            if type(response) == str:
                if response == "load chosen option": 
                    current_prompt = current_prompt.next_prompt()
                    
                elif response == "validate login":
                    username = current_prompt.entered_username
                    password = current_prompt.entered_password
                    
                    # Validate login given username and password
                    user_found = users.validate_login(username, password) 
                    if user_found != None: # If user exists, load next prompt    
                        session = user_found                        
                        USER_PROFILE = "admin_profile" if session.id == 0 else "user_profile"
                        
                        current_prompt = UserProfilePrompt(USER_PROFILE)
                        
                # Sign up user and check if everything is alright
                elif response == "validate sign up": 
                    successfully_signed_up = users.sign_up_user(current_prompt.entered_values,
                                                                data_path=PROJECT_ROOT / PATH_USERS_DATA_CSV)
                    if successfully_signed_up:  
                        current_prompt = LoginPrompt("login")
                
                
                elif response == "load user profile":
                    current_prompt = UserProfilePrompt(USER_PROFILE)
                   
                    
                elif response == "terminate":
                    users.rewrite_csv()
                    articles.write_metadata()
                    exit()
                
                
                elif response == "search keywords":
                    keywords = current_prompt.keywords
                    found_articles = model.search(articles=articles,
                                                  keywords=keywords,
                                                  quantity=5)
                    clear_screen()
                    
                    current_prompt = ArticleListing(articles=found_articles,
                                                    show_delete=False,
                                                    show_stats=True,
                                                    saved_articles=False)
                    
                # Button responses from an article
                elif response in ARTICLE_RESPONSES:
                    
                    article_id = current_prompt.id # Will be used as parameter
                    users_csv_modified        = False
                    article_metadata_modified = False
                    if response == "like":
                        new_like_added = articles.like(article_id=article_id,
                                                       user=session)
                        
                        users_csv_modified        = (users_csv_modified or new_like_added)
                        article_metadata_modified = (article_metadata_modified or new_like_added)
                        
                        
                    if response == "recommend":
                        # Recommend top 10 similar articles
                        articles_recommended = model.recommend(article_id=article_id,
                                                               quantity=10)
                      
                        # Select one recommendation randomly
                        random_idx = int(np.random.randint(low=0, 
                                                           high=10))
                        
                        # Get the random top-10 generation
                        random_article_id = int(articles_recommended[random_idx])
                        
                        # Show the recommendation
                        current_prompt = articles[random_article_id]
                        
                        
                    elif response == "dislike":
                        new_dislike_added = articles.dislike(article_id=article_id,
                                                             user=session)
                        
                        users_csv_modified = (users_csv_modified or new_dislike_added)
                        article_metadata_modified = (article_metadata_modified or new_dislike_added)
                        
                        
                    elif response == "save":
                        new_article_saved = articles.save(article_id=article_id,
                                                          user=session)
                        
                        users_csv_modified = (users_csv_modified or new_article_saved)
                        
                    # If there is some modification to user data, 
                    # change the csv as needed to keep up with updates
                    if users_csv_modified:
                        users.rewrite_csv()
                        
                    if article_metadata_modified:
                        articles.write_metadata()
                   
                    
                elif response in USER_PROFILE_RESPONSES:
                    if response == "Add New Article":
                        # Hell to implement
                        current_prompt = AddNewArticlePrompt("add_new_article") 
                        
                    
                    elif response == "Search Articles":
                        # Heaven to implement
                        current_prompt = SearchPrompt("search") 
                    
                    
                    elif response == "My Articles":  
                        if session.id == 0:
                            articles_created = articles.articles.copy()
                        else:
                            articles_created = [articles[idx] for idx in session.articles_created]
                            
                        current_prompt = ArticleListing(articles=articles_created,
                                                        show_delete=True,
                                                        show_stats=True,
                                                        saved_articles=False,
                                                        admin=(session.id == 0))
                    
                    
                    elif response == "Saved Articles":
                        articles_saved = [articles[idx] for idx in session.articles_saved]
                        current_prompt = ArticleListing(articles=articles_saved,
                                                        show_delete=True,
                                                        saved_articles=True)
                    
                    
                    elif response == "Platform Statistics (Interactions)":
                        articles.show_platform_statistics_interactions(num_users=len(users))
                        
                    
                    elif response == "Platform Statistics (Tags)":
                        articles.show_platform_statistics_tags(keywords=model.features)
                    
                    elif response == "Exit":
                        exit()
                        
                        
                elif response == "new article ready":
                    new_article_data = current_prompt.entered_values
                    
                    # Add new article to the collection
                    articles.add_new_article(new_article_data=new_article_data)
                    
                    # Add created article to the list of curren't users articles
                    users.add_new_article(new_article=articles.articles[-1],
                                          user_id=session.id)
                    
                    # Refit the model to account for new article
                    model.refit(articles=articles)
                    
                    # Return back to the User Profile Prompt
                    current_prompt = UserProfilePrompt(USER_PROFILE)
                    
            
            # Case of Article Listing Response
            if (isinstance(response, tuple) and
                len(response) == 2 and 
                isinstance(response[0], str) and 
                isinstance(response[1], int)):
                
                option_selected, article_id = response

                if option_selected == "show":
                    current_prompt = articles[article_id]
                    current_prompt.increment_views()
                    
                    
                elif option_selected == "delete article":
                    # Remove article from the collection, including the files
                    articles.remove_article(article_id)
                    
                    users.rewrite_csv()
                    session.articles_created.remove(article_id)
                    
                    model.refit(articles)
                    
                    # Return back to the User Profile Prompt
                    current_prompt = ArticleListing(articles=articles,
                                                    show_delete=True,
                                                    saved_articles=False)
                    
                    
                elif option_selected == "delete from saved":
                    session.articles_saved.remove(article_id) 
                    users.rewrite_csv()
                    
                    new_articles_saved = [articles[idx] for idx in session.articles_saved]
                    current_prompt = ArticleListing(articles=new_articles_saved,
                                                    show_delete=True,
                                                    saved_articles=True)
                    
                elif option_selected == "show statistics":
                    article_selected = articles[article_id]
                    article_selected.show_statistics()



if __name__ == "__main__":
    setup() # Setup everything necessary for program's intended functionality
    main()  # Call the main drawing loop