import os
import csv
import shutil
from nltk.tokenize import sent_tokenize
from tempfile import NamedTemporaryFile

''' This file will allow me to:
- read a .txt from a specified subfolder
- create a sentence-tokenized version
- scroll from the beginning and end to find the first and last sentences
- write a csv with the file path and proper indexes for the beginning and end of the book

This file deals with the issue of the imported .txt files coming with lots of additional text regarding it's source
as well as tables of contents that would inevitably throw off the word counts during the analysis. By compiling the 
index markings fort he true beginning and ending into a simple csv for Books_exp.py to utilize, it makes the process 
of adding new books easy, requiring only a brief interation through this file and running books_exp.py once afterwards.
'''

def main():
    while True:
        # Gather pathways to both the folder of .txt files and books.csv
        script_dir = os.path.dirname(__file__)
        folder = 'Books'
        csv_file = 'books.csv'
        folder_path = os.path.join(script_dir, folder)
        csv_path = os.path.join(script_dir, csv_file)
# NOTE Merge below into one line?
        books = os.listdir(folder_path)
        books = [x for x in sorted(books) if ".txt" in x]

        # Gather current books.csv into a list of dicts
        if not os.path.isfile(csv_path):
            f = open("books.csv", "w")
        with open(csv_path, 'r') as f:
            dict_reader = csv.DictReader(f)
            range_list = list(dict_reader)

        # Present list of options, marking which files have already been processed adn storing their entered status in a 
        # list of bools (each value in entered will match it's respective index number in books)

# TODO NOTE turn below into choose_book(books, range_list) function
        # NOTE This might be easier to do by building a list of dicts with a for loop. It would be functionally the same but
        # probably less prone to errors if the values are actually connected in the same object, rather than just sharing index numbers
        entered = []
        print("Choose from the following file names or type 'EXIT' to exit:\n")
        i = 0
        for b in books:
            if any(b in e['File Name'] for e in range_list):
                entered.append(True)
                print(f"(ENTERED) {i}: {b}")
            else:
                entered.append(False)
                print(f"{i}: {b}")
            i += 1
        
        # Validate input
        # NOTE This is super barebones validation, more for catching typos than maliciousness.
        index = input("\nBook index number: ")
        if index == 'EXIT':
            break
        elif not index.isnumeric:
            print("Invalid input, let's try again")
            continue
        try:
            this_book = books[int(index)]
        except TypeError:
            print("That number wasn't a listed option you lunatic, back to start with you!")
        book = os.path.join(folder_path, this_book)

        # Double check with user if selection has already been entered
        if entered[int(index)]:            
            redo = choose("\nBook range already entered, redo entry? (Y/N):",'Y','N')
            if redo == 'N':
                continue
# TODO NOTE END choose_book()

# TODO NOTE create new class (not book, already used in books.py and it that would be confusing) and use this as the __init__
        # Gather text as list of sentences
        with open(book) as f:
            contents = f.read()
        sent_list = sent_tokenize(contents)


# NOTE Review the following link to make this more concise: https://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response
# And review this one for how to make these functions class methods: https://stackoverflow.com/questions/32721580/example-of-class-with-user-input

# TODO NOTE already started scroll function as new_func(), needs 
        # Scroll to find the first sentence using terminal commands
        print("Hit enter without input to view next sentence, or type the number of sentences you wish to scroll by(negative numbers will scroll backwards), until the true first sentence is found. If first sentence is found, type '!'. If you need to exit and return to book select, type '?'. To reload the book, type'#.")
        i = 0
        found = False
        while not found:
            # Catch indices outside of the range, INCLUDING negative numbers which I forgot reverse indexes the list
            if not 0 <= i < len(sent_list):
                print("\n!!! You've scrolled too far! Back to the start with you, you filthy mongrel !!!\n")
                i=0
                continue

            # Move forward by one index number
            mark = input(f"\n{sent_list[i]}\n")
            if mark == '':
                i += 1
                continue
            # Move forward by variable number
            elif mark.isnumeric():
                i += int(mark)
                continue
            # Restart the selection process after updating the sent_list
# NOTE This is for editing fluff out of the first and last sentences if formatting issues cause them to be inaccurate,
# I just have to open the txt file in another tab, edit it, and use this command to come back to the same spot in the edited file
# TODO NOTE MUST BE ADDED to new_func, but needs the new class first.
            elif mark == '#':
                with open(book) as f:
                    contents = f.read()
                sent_list = sent_tokenize(contents)
                continue
            # Mark the index as the begining.
            elif mark == '!':
                found = True
                first = i
                continue     
            # Return to book selection      
            elif mark == '?':
                break
            else:
                print('Invalid input, try again!')
                continue
# NOTE pretty sure the below is uneccesary, turning it off and we'll see what happens!
        # if not found:
        #     continue

        print("Hit type '.' to view previous sentence, or type the number of sentences you wish to scroll by (negative numbers will scroll backwards), until the true last sentence is found. If last sentence is found, type '!'. If you need to exit and return to book select, type '?'")
        i = len(sent_list) - 1
        found = False
        while not found:
            if not 0 <= i < len(sent_list):
                print("\n!!! You've scrolled too far! Back to the start with you, you filthy mongrel !!!\n")
                i = len(sent_list) - 1
                continue
            mark = input(f"\n{sent_list[i]}\n")
            if mark == '':
                i -= 1
                continue
            elif mark == '?':
                break
            elif mark == '#':
                with open(book) as f:
                    contents = f.read()
                sent_list = sent_tokenize(contents)
                continue
            elif mark == '!':
                found = True
                last = i
                continue
            elif mark.isnumeric:
                i -= int(mark)
                continue
            else:
                print('Invalid input, try again!')
                continue
        if not found:
            break


# TODO NOTE These can all be functs or methods depending on whether I choose to make a second new class or not
        print("\nRanges input successfully! Now for additional info:\n")
        author = input("Author full name: ")
        title = input("\nFull book title: ")
# TODO NOTE Turning below into get_genre()
        print("\nInput the index number for the proper genre\n")
        g_opts = ["Sci-Fi", "Horror", "Adventure", "Fantasy", "Mystery", "Western"]
        genres = []
        while True:
            i = 0
            for g in g_opts:
                print(f"{i}: {g}")
                i += 1
            pick = input("\nInput: ")
            if pick == '':
                break
            if pick not in [str(x) for x in range(len(g_opts))]:
                print("Invalid input, try again!")
                continue
            genres.append(this := g_opts[int(pick)])
            g_opts.remove(this)

            more = choose("Select another genre? (Y/N): ",'Y','N')
            if more == 'Y':
                continue
            else:
                break
        correct = choose(f"- Entry -\nAuthor: {author}\nTitle: {title}\nGenre(s): {', '.join(genres)}\n\nIs this correct?(Y/N): ",'Y','N')
        if correct == 'N':
                print("Oopsie Poopsie, let's try that again!\n")
                continue 

# NOTE TODO After streamlining, I want to consider merging this and books.py into one file and remove the intermediary csv step.
        # Either update and replace the old row using a temporary file, or simply append the new row
        entry = {'File Name':this_book, 'Title':title, 'Author':author, 'Genre':", ".join(genres), 'First Sentence':first, 'Last Sentence':last}
        if entered[int(index)]:
            tempfile = NamedTemporaryFile(mode='w', delete=False)
            with open('books.csv', 'r') as csvfile, tempfile:
                reader = csv.DictReader(csvfile, fieldnames=entry.keys())
                writer = csv.DictWriter(tempfile, fieldnames=entry.keys())
                for row in reader:
                    if row['File Name'] == this_book:
                        print('updating row', this_book)
                        writer.writerow(entry)  
                    else:
                        writer.writerow(row)
            shutil.move(tempfile.name, 'books.csv')
        else:
            with open('books.csv', 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=entry.keys())
                if os.stat('books.csv').st_size == 0:
                    writer.writeheader()
                writer.writerow(entry)
        
        # Check if user wants to continue and end program if not.
        cont = choose("\nEntry complete! Continue? (Y/N):",'Y','N')
        if cont == 'Y':
            continue
        elif cont == 'N':
            break

def choose(prompt, arg1, arg2):
    """
    Choose automates asking a prompt in a while loop to allow reprompting, returning only one of the correct options
    It can't be broken except by inputing one of the correct options 
    """

    tries = 0
    while True:
        if tries == 3:
            print("Warning! One more improper input and the program will exit. I believe in you!")
        if tries == 4:
            raise UserShenanigans
        choice = input(prompt).strip()
        if choice not in [arg1, arg2]:
            print(f"\nInvalid input. Please only input one of the stated options ( {arg1} , {arg2} ) exactly as written (case sensitively!)\n")
            tries += 1
            continue
        else:
            break
    if choice == arg1:
        return arg1
    else:
        return arg2
    
# Testing turning the scrolling feature into a single function, looks good so far
def get_range(scrl, spot):
    if not isinstance(scrl, Scroller):
            raise Exception("Tried to create a card with an improper input.")
    print("Hit type '.' to view previous sentence, or type the number of sentences you wish to scroll by (negative numbers will scroll backwards), until the true last sentence is found. If last sentence is found, type '!'. If you need to exit and return to book select, type '?'")
    i = 0 if spot == 'front' else len(scrl.sents) - 1
    found = False
    while not found:
        if not 0 <= i < len(scrl.sents):
            print("\n!!! You've scrolled too far! Back to the start with you, you filthy mongrel !!!\n")
            i = 0 if spot == 'front' else len(scrl.sents) - 1
            continue
        mark = input(f"\n{scrl.sents[i]}\n")
        if mark == '':
            i += 1 if spot == 'front' else -1
            continue
        elif mark == '?':
            break
        elif mark == '!':
            found = True
            index = i
            continue
        elif mark.isnumeric:
            i += int(mark) if spot == 'front' else -(int(mark))
            continue
        else:
            print('Invalid input, try again!')
            continue
    if not found:
        return None
    return index

# Testing turning book selection into single function
#NOTE I'm breaking choose_book into two functions, list_books
def list_books(books, range_list):
    print("Choose from the following file names or type 'EXIT' to exit:\n")
    library = []
    i = 0
    for b in books:
        file = {'file':b}
        if any(b in e['File Name'] for e in range_list):
            file['entered':True]
            print(f"{i}: {b} (entered)")
        else:
            file['entered':False]
            print(f"{i}: {b}")
        library.append(file)
        i += 1
        
# NOTE Still needs to be set in a while loop on the outside, with EXIT causing break and CONT causing continue
def get_book(library, folder_path):
    # Validate input
    # NOTE This is super barebones validation, more for catching typos than maliciousness.
    index = input("\nBook index number: ")
    if index == 'EXIT':
        return index
    elif not index.isnumeric:
        print("Invalid input, let's try again")
        return "CONT"
    try:
        this_book = library[index]['file']
    except TypeError:
        print("That number wasn't a listed option you lunatic, back to start with you!")

    # Double check with user if selection has already been entered
    if library[index]['entered']:            
        redo = choose("\nBook range already entered, redo entry? (Y/N):",'Y','N')
        if redo == 'N':
            return "CONT"
    
    return os.path.join(folder_path, this_book)

def get_genre():
    print("\nInput the index number for the proper genre\n")
    g_opts = ["Sci-Fi", "Horror", "Adventure", "Fantasy", "Mystery", "Western"]
    genres = []
    while True:
        i = 0
        for g in g_opts:
            print(f"{i}: {g}")
            i += 1
        pick = input("\nInput: ")
        if pick == '':
            return "SKIP"
        if pick not in [str(x) for x in range(len(g_opts))]:
            print("Invalid input, try again!")
            continue
        genres.append(this := g_opts[int(pick)])
        g_opts.remove(this)

        more = choose("Select another genre? (Y/N): ",'Y','N')
        if more == 'Y':
            continue
        else:
            return genres

class Scroller:
    def __init__(self, path):
        if not isinstance(path, str):
            raise UserShenanigans("This Scroller object was initialized with an invalid path. Personally, I feel like it's more your fault than mine")
        self.path = path
        self.txt = None
        self.sents = None
        self.load()

    def load(self):
        with open(self.path) as f:
            self.txt = f.read()
        self.sents = sent_tokenize(self.txt)

class UserShenanigans(Exception):
    def __init__(self):
        self.message = "Program exitted due to excessive silliness(you know what you did). It's been a pleasure nonetheless!"
    def __str__(self):
        return self.message  
    
if __name__ == "__main__":
    main()