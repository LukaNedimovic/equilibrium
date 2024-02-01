class ArticleListing:
    def __init__(self, 
                 articles: list,
                 show_delete: bool = False,
                 show_stats:  bool = False,
                 saved_articles: bool = False,
                 admin: bool = False):
        """
        Creates an instance of ArticleListing.

        Parameters
        ----------
        articles : list
            List of Article-s to be shown
        show_delete : bool, optional
            If true, will show delete button.
        saved_articles : bool, optional
            Article listing can be used for saved articles too.
            If this is true, it indicated that. 
            Will be useful when differentiating from where to delete an article.
        """
        
        self.articles       = articles
        self.show_delete    = show_delete
        self.saved_articles = saved_articles
        self.show_stats     = show_stats
        
        self.radio_selection_row = 0
        self.radio_selection_col = 0
        self.radio_selection_size = len(self.articles)
        
        self.radio_selection_cols = 1 + show_delete + show_stats
        
        self.admin = admin
        
    
    def show(self):
        """
        Renders an ArticleList.
        """
        
        for idx, article in enumerate(self.articles):
            # In case there are invalid articles, just skip them
            if article is None:
                continue
            
            # If current row being rendered is selected
            if idx == self.radio_selection_row:   
                
                # 0 - article button
                # 1 - delete button
                # 2 - statistics button
                
                if self.radio_selection_col == 0:
                    article.show_article_as_list_element(show_delete=self.show_delete,
                                                         show_stats=self.show_stats,
                                                         bolded_article=True)
                    
                elif self.show_delete and self.radio_selection_col == 1:
                    article.show_article_as_list_element(show_delete=self.show_delete,
                                                         show_stats=self.show_stats,
                                                         bolded_delete=True,
                                                         bolded_stats=False)
                    
                elif self.show_stats and self.radio_selection_col == 2:
                    article.show_article_as_list_element(show_delete=self.show_delete,
                                                         show_stats=self.show_stats,
                                                         bolded_delete=False,
                                                         bolded_stats=True)
            
            # Otherwise, just show plain article
            else:
                article.show_article_as_list_element(show_delete=self.show_delete,
                                                     show_stats=self.show_stats)
            
            
    def parse_keypress(self, key: str):
        """
        Parse keypress hit while the ArticleListing was present.
        
        Parameters
        ----------
        key : str
            Key pressed while the ArticleListing was present - to be parsed.
        
        Returns
        -------
        (...):
            In case of "enter" being hit, will send "show" or "delete", 
            with article's id.
            In case of "escape" being hit, will send "load user profile".
            Otherwise, will send None.
        """
        response = None # Default response


        if key == "up": 
            self.radio_selection_row -= 1 # Move radio selection for one upwards
            if self.radio_selection_row== -1: # If there is nothing on top
                # Move selection to the last possible field / on the end
                self.radio_selection_row = self.radio_selection_size - 1

        elif key == "down": # Similar to the "up" case
            self.radio_selection_row += 1
            if self.radio_selection_row == self.radio_selection_size:
                self.radio_selection_row = 0
                
        elif key == "left":
            self.radio_selection_col -= 1
            if self.radio_selection_col < 0:
                self.radio_selection_col = 1
            
        elif key == "right":
            self.radio_selection_col += 1
            if self.radio_selection_col == self.radio_selection_cols:
                self.radio_selection_col = 0

        elif key == "enter": # Open chosen option's prompt
            article_selected = self.articles[self.radio_selection_row].id
            option_selected = "show"
            if self.show_delete and self.radio_selection_col == 1:
                if self.saved_articles:
                    option_selected = "delete from saved"
                else:
                    option_selected = "delete article"
                    
            if self.show_stats and self.radio_selection_col == 2:
                option_selected = "show statistics"
                    
            response = (option_selected, article_selected)
            
        elif key == "escape" or key == "esc":
            response = "load user profile"
            
            
        return response
