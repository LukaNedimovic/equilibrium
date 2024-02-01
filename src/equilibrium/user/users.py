from user.user import User

from utils.data_wrapper import DataWrapper
from utils.parser import parse_csv, write_line_csv

from article.article import Article

class Users:
    def __init__(self, 
                 path_users_data=""):
        """
        Creates an instance of Users.
        """
        
        self.path_users_data = path_users_data
        
        self.users = []


    def __getitem__(self, arg) -> User:
        return self.users[arg]
    
    def __len__(self):
        return len(self.users)
    
    
    def load(self):
        """
        Function that loads users into the "users" list.
        The point of this loading is to optimize time and space ->
        it is better to have everything loaded once (if not too large) and then
        query it when the time is needed.
        """
        
        print("[Users Wrapper]: Starting to load users.")
        # Parse CSV file containing user data, and place the data inside wrapper
        user_data_parsed = parse_csv(self.path_users_data) 
        user_data_wrapped = DataWrapper(user_data_parsed)

        
        for row in user_data_wrapped.data: # For each row that is not a column names
            new_user = User(row) # Create a user out of singular row
            self.users.append(new_user) # Add it to the users list
        
        
        print("[Users Wrapper]: Users loaded successfully.")
        
        # Print all the users
        #for user in self.users:
        #   print(user)    
            

    def validate_login(self, username: str, password: str) -> User:
        """
        Function that checks whether a User with given username and password
        exists inside the database. 
        Database is already loaded, however, so there is no need to open the
        file and parse it all over again.

        Parameters
        ----------
        username : str
            Username entered in the Login prompt.
        password : str
            Password entered in the Login prompt.

        Returns
        -------
        User
            Returns complete User object if user is found.
            Otherwise, returns None.
        """
        
        found_user = None
        for user in self.users:
            if (user.username == username and user.password == password):
                found_user = user
                break
            
        return found_user
        #return any((user.username == username and user.password == password) 
        #           for user in self.users)
    
    def username_exists(self, username: str) -> bool:
        """
        Checks whether there is already a registered username - no two users
        can have the same username.

        Parameters
        ----------
        username : str
            Username to be checked.

        Returns
        -------
        bool
            Whether the given username already exists in the database.
        """
        
        return any((user.username == username) for user in self.users)

    def sign_up_user(self, user_data: dict, data_path: str) -> bool:
        """
        Attempts at signing up the user.

        Parameters
        ----------
        user_data : dict
            All relevant data for new user.

        Returns
        -------
        bool
            Whether the user has been successfully signed up.
        """
        
        # print(user_data) 
        
        # Check whether the given username already exists in the database
        if self.username_exists(user_data["username"]): 
            return False
        
        else: # If it does not
            user = User(user_data)    # Create a new user baed on data
            user.id = len(self.users) # Assign them an ID, also
            
            # Write their data into the database (in our case just a ".csv")
            write_line_csv(data_path, user.to_csv_row())             
            # Add the new user into the already existing collection - 
            # no need to parse everything all over again."
            self.users.append(user) 
            return True
        
        
    def rewrite_csv(self):
        """
        Rewrites completely users metadata .csv file.
        """
        
        column_names = None
        with open(self.path_users_data, "r", encoding="utf8") as users_csv:
            column_names = users_csv.readline()


        with open(self.path_users_data, "w", encoding="utf8") as users_csv:
            users_csv.write(column_names)
            for user in self.users:
                users_csv.write(user.to_csv_row())
                
                
    def add_new_article(self, new_article: Article, user_id: int):
        """
        Adds a new article to the respectable user, then updates the user
        metadata .csv file.

        Parameters
        ----------
        new_article : Article
            New article created.
        user_id : int
            ID of user who created the article.
        """
        
        self.users[user_id].articles_created.append(new_article.id)
        self.rewrite_csv()
        
