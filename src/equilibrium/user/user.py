import ast

class User:
    def __init__(self, user_data: dict):
        """
        Creates an instance of User.

        Parameters
        ----------
        user_data : dict
            All relevant data to a singular user.

        """
        
        # All "keys" represent the properties to be loaded into the object
        for key, value in user_data.items():
            setattr(self, key, value)
        
        if "id" in user_data:
            self.id = ast.literal_eval(self.id)
        
        if "articles_created" in user_data:
            self.articles_created = self.articles_created[1:-1]
            self.articles_created = ast.literal_eval(self.articles_created) 
        else:
            self.articles_created = []
        
        if "articles_liked" in user_data:
            self.articles_liked = self.articles_liked[1:-1]
            self.articles_liked = ast.literal_eval(self.articles_liked)  
        else:
            self.articles_liked = []
            
        if "articles_disliked" in user_data:
            self.articles_disliked = self.articles_disliked[1:-1]
            self.articles_disliked = ast.literal_eval(self.articles_disliked)   
        else:
            self.articles_disliked = []
                
        if "articles_saved" in user_data:
            self.articles_saved = self.articles_saved[1:-1]
            self.articles_saved = ast.literal_eval(self.articles_saved)     
        else:
            self.articles_saved = []
            
        
    def __str__(self) -> str:
        return (
            f"{self.id},"
            f"{self.username},"
            f"{self.password},"
            f"{self.name},"
            f"{self.surname},"
            f"{self.date_of_birth},"
            f"{self.residence},"
            f'"{str(self.articles_created)}",'
            f'"{str(self.articles_liked)}",'
            f'"{str(self.articles_disliked)}",'
            f'"{str(self.articles_saved)}"'
            f"\n"
        )
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def to_csv_row(self) -> str:
        """
        Returns a comma-separated representation of the user's data.

        Returns
        -------
        str
            Comma-separated values of user's data.
            This can be then written into ".csv" easily, if needed.
        """
    
        return self.__str__()