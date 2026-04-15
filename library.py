import sys
import json

libraryDatabase = []
libraryFile = 'library.json'

try: 
    with open(libraryFile) as f: 
        libraryDatabase = json.load(f)
except (FileNotFoundError, json.JSONDecodeError): 
        libraryDatabase = []



def menu():
    print('[ Welcome to the Library ]')
    while True: 
        print('--Library Menu--')
        print('1. Add a book')
        print('2. View all books')
        print('3. Search books')
        print('4. Exit Library')

        response = input('select option: ')
        
        if response == '1':
            while True:  
                response = input('Would you like to add a book?(y/n): ').lower()
                if response == 'n':
                    break
                if response == 'y': 
                    addBooks()
                else: 
                    print('*error, incorrect selection\n')
        elif response == '2':
            viewBooks()
        elif response == '3':
            print('\n---Seach for Books---')
            title = input("enter title of book you'd like to search('q' to quit): ").lower()
            searchBooks(title)
        elif response == '4':
            sys.exit()
        else: 
            print('*error, incorrect selection\n')
    
def addBooks():
    print('\n---Add a Book Here!---')
    title = input('enter title of book: ')
    author = input('enter author: ')

    while True:
        year = input('enter year published: ')
        try: 
            year = int(year)
            break
        except:
            print('*error, must enter a year*\n')
            
    while True: 
        availability = input('enter book status(type available): ').lower()
        if availability != 'available':
            print('*error, incorrect selection\n')
        else:
            break

    book = {
    "title": title,
    "author": author,
    "year": year,
    "availability": availability
    }

    libraryDatabase.append(book)

    # open/create json, use writing mode, set file as f, and dump data into json
    saveLibrary()

    print(f"{book['title']} added!\n")
    

def viewBooks(): 
    count = 1
    print('\n---Viewing All Books---')
    if len(libraryDatabase) < 1: 
        print('no books on display...\n')
        return
    for book in libraryDatabase:
        print(f'{count}.')
        print(f'Book title: {book["title"]} \nAuthor: {book["author"]} \nYear: {book["year"]} \nAvailability: {book["availability"]}\n')
        count += 1

def searchBooks(title):
    count = 1

    print('\n-Books-')
    matches = [] # create a list for match books 

    # loop to go through database and retrieve search results 
    for book in libraryDatabase:
        if title in book['title'].lower():
            matches.append(book) 

    # check if there is any books in matches        
    if len(matches) < 1: 
        print('book not found\n')
        return 
    
    # loop through matches and print
    for book in matches:
            print(f'{count}.')
            print(f'Book title: {book["title"]} \nAuthor: {book["author"]} \nYear: {book["year"]} \nAvailability: {book["availability"]}\n')
            count += 1

    # let user select from matches
    while True:
        bookSelected = input("enter the numbered book you'd like to select('q to go back to menu'): ")
        if bookSelected == 'q':
            return None
        try: 
            bookSelected = int(bookSelected) # convert input to int 
            # check correct user input 
            if bookSelected < 1 or bookSelected > len(matches): 
                print('error, incorrect selection\n')
                continue
            selectedBook = matches[bookSelected - 1] # 0 started index so we fixed it here
            break 
        except:
            print('*error, enter number\n')

    # allow user to checkout or return
    while True:
        response = input(f"would you like to checkout, return, or delete {selectedBook['title']} ('q' to exit): ").lower()     
        if response == 'checkout':
            checkout(selectedBook)
            break
        elif response == 'return':
            returnBook(selectedBook)
            break
        elif response == 'delete': 
            deleteBook(selectedBook)
            break
        elif response == 'q':
            break
        else:
            print('*error\n')


def checkout(selectedBook):
    print('\n---Check Out a Book---')

    # user should not be able to check out book that is unavailable
    if selectedBook["availability"] == "unavailable": 
        print('*error, this book is already checked out\n')
        
    elif selectedBook["availability"] == 'available': 
        selectedBook["availability"] = "unavailable"
        print(selectedBook['title'], 'has now been checkout...\n')
        # update library database
        saveLibrary()


def returnBook(selectedBook): 
    print('\n---Return Book---')
    
    # user should not be able to return book that is availabile
    if selectedBook["availability"] == 'unavailable':
        selectedBook["availability"] = 'available'
        print(selectedBook['title'], 'has been returned...\n' )
        # update library database
        saveLibrary()
    elif selectedBook["availability"] == 'available':
        print('*error, book has already been returned\n') 

def deleteBook(selectedBook): 
    print('\n---Delete Book---')

    if selectedBook["availability"] == 'unavailable': 
        print('Can not delete a book that is unavailable\n')
        return
    
    libraryDatabase.remove(selectedBook)
    print(f"{selectedBook['title']} has been deleted...\n" )
    saveLibrary()

def saveLibrary(): 
    with open(libraryFile, "w") as f: 
        json.dump(libraryDatabase, f)

            


menu()