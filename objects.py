# objects.py
# Copyright Team 0xC0DEBABE™ 2020 

class Scenario:
    def __init__(self, libraries, books, days):
        self.libraries = libraries # array of Library objects
        self.books = books # array of Book objects
        self.days = days

class Library:
    def __init__(self, id, books, signup_time, books_per_day):
        self.id = id # index
        self.books = books # array of Book objects
        self.signup_time = signup_time
        self.books_per_day = books_per_day

        self.gann_score = 0 # for use in GANN solution
        
class Book:
    def __init__(self, id, score):
        self.id = id # index
        self.score = score