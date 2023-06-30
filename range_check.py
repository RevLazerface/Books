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

# NOTE This file could definitely be streamlined. Maybe with classes, maybe with functions, maybe both, but it's
# past 1am so that's a problem for you, future Nick, you handsome devil you

def main():
    while True:
        # Gather pathways to both the folder of .txt files and books.csv
        script_dir = os.path.dirname(__file__)
        folder = 'Books'
        csv_file = 'books.csv'
        folder_path = os.path.join(script_dir, folder)
        csv_path = os.path.join(script_dir, csv_file)
        books = os.listdir(folder_path)

        # Gather current books.csv into a list of dicts
        if not os.path.isfile(csv_path):
            f = open("books.csv", "w")
        with open(csv_path, 'r') as f:
            dict_reader = csv.DictReader(f)
            range_list = list(dict_reader)

        # Present list of options, marking which files have already been processed
        x = 0
        entered = []
        print("Choose from the following file names or type 'EXIT' to exit:\n")
        for b in books:
            if any(b in e['File Name'] for e in range_list):
                entered.append(True)
                print(f"{x}: {b} (entered)")
            else:
                entered.append(False)
                print(f"{x}: {b}")
            x += 1
        
        # Validate input
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
            while True:
                redo = input("\nBook range already entered, redo entry? (Y/N):")
                if redo not in ['Y','N']:
                    print('invalid input, try again!')
                    continue
                else:
                    break
            if redo == 'N':
                continue

        # Gather text as list of sentences
        with open(book) as f:
            contents = f.read()
        sent_list = sent_tokenize(contents)

        # Scroll to find the first sentence using terminal commands
        print("Hit enter without input to view next sentence, or type the number of sentences you wish to scroll by(negative numbers will scroll backwards), until the true first sentence is found. If first sentence is found, type '!'. If you need to exit and return to book select, type '?'")
        i = 0
        found = False
        while not found:
            if not 0 <= i < len(sent_list):
                print("\n!!! You've scrolled too far! Back to the start with you, you filthy mongrel !!!\n")
                i=0
                continue
            mark = input(f"\n{sent_list[i]}\n")
            if mark == '':
                i += 1
                continue
            elif mark == '?':
                break
            elif mark == '!':
                found = True
                first = i
                continue
            elif mark.isnumeric:
                i += int(mark)
                continue
            else:
                print('Invalid input, try again!')
                continue
        if not found:
            break

        # NOTE This should be a function maybe? I'm using it twice in a row with only minor changes
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

        # TODO After picking index ranges, enter additional info like author's full name and genre
        # NOTE my validate_input function from the flashcards project can help here
        print("\nRanges input successfully! Now for additional info:\n")
        while True:
            author = input("Author full name:")
            correct = input(f"Is {author} correct? (Y/N):")
            if correct not in ['Y','N']:
                print('invalid input, try again!')
                continue
            elif correct == 'N':
                continue
            else:
                break

        while True:
            title = input("\nFull book title:")
            correct = input(f"Is {title} correct? (Y/N):")
            if correct not in ['Y','N']:
                print('invalid input, try again!')
                continue
            elif correct == 'N':
                continue
            else:
                break
            
        while True:
            genres = ["Sci-Fi", "Fantasy", "Humor", "Romance", "Crime", "Western"]
            print("\nInput the index number for the proper genre\n")
            i = 0
            for g in genres:
                print(f"{i}: {g}")
                i += 1
            pick = input("\nInput: ")
            if pick not in ['0','1','2','3','4','5']:
                print("Invalid input, try again!")
                continue
            correct = input(f"Is {genres[int(pick)]} correct? (Y/N):")
            if correct not in ['Y','N']:
                print('invalid input, starting over!')
                continue
            elif correct == 'N':
                continue
            else:
                break


        # Either update and replace the old row using a temporary file, or simply append the new row
        entry = {'File Name':this_book, 'Title':title, 'Author':author, 'Genre':genres[int(pick)], 'First Sentence':first, 'Last Sentence':last}
        if entered[int(index)]:
            tempfile = NamedTemporaryFile(mode='w', delete=False)
            with open('books.csv', 'r') as csvfile, tempfile:
                reader = csv.DictReader(csvfile, fieldnames=entry.keys())
                writer = csv.DictWriter(tempfile, fieldnames=entry.keys())
                for row in reader:
                    if row['File Name'] == this_book:
                        print('updating row', this_book)
                        row['first_sent'], row['last_sent'] = entry['first_sent'], entry['last_sent'] 
                    row = {'File Name':row['File Name'], 'first_sent':row['first_sent'], 'last_sent':row['last_sent']}   
                    writer.writerow(row)
            shutil.move(tempfile.name, 'books.csv')
        else:
            with open('books.csv', 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=entry.keys())
                writer.writeheader()
                writer.writerow(entry)
        
        # Check if user wants to continue and end program if not.
        while True:
            cont = input("\nEntry complete! Continue? (Y/N):")
            if cont not in ['Y','N']:
                print('invalid input, try again!')
                continue
            else:
                break
        if cont == 'Y':
            continue
        elif cont == 'N':
            break
    
if __name__ == "__main__":
    main()