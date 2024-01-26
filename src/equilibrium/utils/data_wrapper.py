class DataWrapper:
    def __init__(self, data):
        """
        Creates a simple wrapper for ".csv" files data after being loaded.

        Parameters
        ----------
        data : 
            Data loaded from the ".csv" file.

        """
        
        # TODO: Find datatype of "data"
        self.column_names = data[0]  # column names
        self.data         = data[1:] 
        
        self.shape = (len(self.column_names), 
                      len(self.data))


    def __getitem__(self, arg) -> dict:
        return self.data[arg]
    
        
    def find_match(self, pattern: dict) -> bool:
        """
        Check whether there is a matching pattern within the loaded data.

        Parameters
        ----------
        pattern : dict
            Check whether every single value given exists as part of the 
            same row.
            This is useful when trying to check whether an entire user exists
            the way they do.

        Returns
        -------
        bool
            Whether such pattern exists within the data loaded - or not.

        """
        for row in self.data:
            if all(row[key] == value for key, value in pattern.items()):
                return True
        return False