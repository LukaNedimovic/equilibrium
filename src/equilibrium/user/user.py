class User:
    def __init__(self, user_data: dict):
        
        for key, value in user_data.items():
            setattr(self, key, value)
        
    def __str__(self):
        return f"{self.surname}, {self.name}"
    
    def __repr__(self):
        return self.__str__()
    
    def to_csv_row(self):
        return f"{self.id},{self.username},{self.password},{self.name},{self.name}{self.surname},{self.date_of_birth},{self.residence},{self.residence}\n"