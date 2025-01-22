class Email_Not_validator(Exception):
    def __init__(self,detail:str):
        self.detail = detail
        