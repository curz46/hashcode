# solve.py
# Copyright Team 0xC0DEBABE™ 2020 - coding breaks are for losers

from os import listdir
from os.path import isfile, join

from objects import *
from simulate import *

days_left = -1

def parse(handle):
    lines = handle.readlines()
    
    header = lines[0].split(" ")
    total_books     = int(header[0])
    total_libraries = int(header[1])
    total_days      = int(header[2])

    books = lines[1].split(" ")
    books = [int(s) for s in books]
    books = [Book(i, score) for (i, score) in enumerate(books)]

    if total_books != len(books):
        print("WARN: total_books(" + str(total_books) + ") does not match len(books)(" + str(len(books)) + ")")

    libraries = []
    library_index = 0
    for i in range(2, len(lines) - 1, 2):
        metadata  = lines[i].split(" ")
        num_books   = int(metadata[0])
        signup_time = int(metadata[1])
        max_per_day = int(metadata[2])
        
        library_books = [int(i) for i in lines[i+1].split(" ")]
        library_books = [books[i] for i in library_books]
        library = Library(library_index, library_books, signup_time, max_per_day)
        
        library_index += 1
        libraries.append(library)

    if total_libraries != len(libraries):
        print("WARN: total_libraries(" + str(total_libraries) + ") does not match len(libraries)(" + str(len(libraries)) + ")")

    #print("Loaded " + str(len(books)) + " books")
    #print("Loaded " + str(len(libraries)) + " libraries")
    print("Scenario will last " + str(total_days) + " days")

    return Scenario(libraries, books, total_days)

def solve(scenario):
    global days_left, library_submissions

    
    # Setup Globals
    days_left = scenario.days
    library_submissions = {}
    
    # Preprocess (prune common books & give initial rating)

    print("Preprocessing...")

    library_scores, _ = preprocess(scenario)
    
    print("Finished preprocessing!")

    print("Solving...")

    # Sort books
    sorted(scenario.books, key=lambda b: b.score)
    for library in scenario.libraries:
        sorted(library.books, key=lambda b: b.score)

    signup_left    = -1 # -1 means not signing up, 0 means just finished
    signup_library = None

    active_libraries = []
    
    while days_left > 0:
        print("Current day: " + str(days_left))
        if signup_left > 0:
            signup_left -=1
            continue
        elif signup_left == 0:
            # Just finished
            active_libraries.append(signup_library)
            signup_left = -1
        
        library_candidates = list(filter(lambda l: l not in active_libraries, scenario.libraries))
        if len(library_candidates) != 0:
            signup_library = evaluate_for_signup(library_candidates)
            signup_left    = signup_library.signup_time
        
        send_books(scenario.libraries)

        # Once this has evaluates, a day has passed
        days_left   -= 1
        signup_left -= 1
        
    print("Solved!")
    
    # Done solving, output
    generate_output_file(active_libraries)
    
    print("Done!")
    
def preprocess(scenario):
    # Steps:
    # 1. Rate each library based on the value of its books
    library_scores = {}
    for library in scenario.libraries:
        score = score_library(library)
        library_scores[library.id] = score
    # 2. 'prune' books from libraries if the book already exists in a higher score library
    best_library_for_book = {}
    i = 0
    for book in scenario.books:
        i += 1
        if i % 500 == 0:
            print("Book: " + str(book.id))
        # Get highest scoring library that contains this book
        best_score    = -1
        best_library  = None
        for candidate_library in scenario.libraries:
            candidate_score = library_scores[library.id]
            if book in candidate_library.books and best_score < candidate_score:
                best_score   = candidate_score
                best_library = candidate_library
        if best_library == None:
            print("WARN: Could not find best library for book " + str(book.id))
        best_library_for_book[book.id] = best_library
    for library in scenario.libraries:
        library.books = list(filter(lambda book: library == best_library_for_book[book.id], library.books))
    # 3. Re-rate each library based on new pruned book contents
    for library in scenario.libraries:
        score = score_library(library)
        library_scores[library.id] = score
    
    print("Done preprocessing")

    return library_scores, best_library_for_book

def evaluate_for_signup(libraries):
    highest_scoring_library = None
    highest_score = -1

    for library in libraries:
        score = score_library(library)
        if(score > highest_score):
            highest_score = score
            highest_scoring_library = library

    return highest_scoring_library

def score_library(library):    
    global days_left    
    shipping_days   = days_left - library.signup_time
        
    score           = 0
    books_shipped   = 0
    days_passed     = 0
        
    for book in library.books:
        if days_passed == shipping_days:
            break

        books_shipped += 1
        if books_shipped == library.books_per_day:
            days_passed += 1
            
        score += book.score
            
    return score

# Takes list of active libaries and updates daily submissions
def send_books(libraries):
    global library_submissions
    print("Sending books for libraries...")
    for library in libraries:
        print("Sending books for library: " + str(library.id))
        #if len(library.books < library.books_per_day):
        #    submissions[library.id].extend(library.books)
        #    library.books = []
        #else:
        submissions = library_submissions[library.id] if library.id in library_submissions else []
        submissions.extend(library.books[:library.books_per_day])
        print("Sent " + str(len(submissions)) + " books.")
        library_submissions[library.id] = submissions
        del library.books[:library.books_per_day]
    print("Done sending books.")
    return

#takes in a list of signed up library objects
def generate_output_file(libraries_signed_up):
    global library_submissions
    filename = "output.txt"
    print("Writing output to '" + filename + "'...")
    with open(filename, "w") as handle:
        handle.write(str(len(libraries_signed_up)) + " \n")
        for library in libraries_signed_up:
            handle.write(str(library.id) + " " + str(len(library_submissions[library.id])) + "\n")
            handle.write(" ".join(str(book.id) for book in library_submissions[library.id]) + "\n")
        handle.close()
    print("Done writing to file.")

def get_file(letter):
    path  = "datasets"
    names = [f for f in listdir(path) if isfile(join(path, f))]
    for name in names:
        if name.startswith(letter + "_"):
            return "datasets/" + name

INPUT_FILE = get_file("b")
WHOSE_WAY = "RAKA"

with open(INPUT_FILE, "r") as handle:
    print("Parsing file '" + INPUT_FILE + "'...")
    scenario = parse(handle)
    print("Done parsing.")
    print("total_books = " + str(len(scenario.books)))
    print("total_libraries = " + str(len(scenario.libraries)))

    if WHOSE_WAY == "RAKA":
        preprocess(scenario)
        import gannsolve
        random_nn = gannsolve.NeuralNetwork([4,8,10,4,1])
        gannsolve.gen_output_file(random_nn, scenario)
    else:
        solve(scenario)