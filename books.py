#import ssl
#import nltk
import csv
import time
import os
from nltk.tokenize import sent_tokenize, word_tokenize
from string import ascii_letters

#NOTE The below code was used to download what I needed from nltk
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

'''
This file will replace b=Books_exp.py, which relied on the nltk.corpus.gutenburg book offerings for it's analysis.
While the corpus module texts get more robust analytical tools, the sample texts are not ideal for my designs.
I can accomplish most of what I got from the corpus module myself using just the tokenizers, allowing me to analize
.txt files downloaded directly from project Gutenberg that aren't in the corpus module. It will:
- Open up the books csv and read it into a custom Book Class object
- Perform adtl processing to get all relevant data
- Enter data into a new csv file
TODO determine exactly what data I actually want to save for each book
TODO design book class (need a brief refresher on class creation)
'''

def main():
    start = time.time()
    # Gather pathways to both the folder of .txt files and books.csv
    script_dir = os.path.dirname(__file__)
    folder = 'Books'
    csv_file = 'books.csv'
    folder_path = os.path.join(script_dir, folder)
    csv_path = os.path.join(script_dir, csv_file)
    file_list = os.listdir(folder_path)

    # Gather current books.csv into a list of dicts
    if not os.path.isfile(csv_path):
        print("CSV doesn't exist! C'mon Future Nick you know it's just you using this, what the heck did you do?")
    with open(csv_path, 'r') as f:
        dict_reader = csv.DictReader(f)
        books_csv = list(dict_reader)

    
    library = []
    for b in books_csv:
        book = Book(b)
        library.append({
                'Title': book.title
                ,'Author': book.author
                ,'Genre': book.genre
                ,'total_characters': sum([get_chars(sent) for sent in book.words])
                ,'total_words': (words := sum([len(sent) for sent in book.words]))  
                ,'total_sentences': len(book.split)
                ,'fs_characters': get_chars(first := word_tokenize(book.first))
                ,'fs_words': len(first)
                ,'ls_characters': get_chars(last := word_tokenize(book.last))
                ,'ls_words': len(last)
                # total vocabulary used divide total words used
                ,'total_vocabulary': (vocab := len(set(sum(book.words, []))))
                ,'vocabulary_rate': round(vocab/words,2)})
    
    keys = library[0].keys()
    with open('books_data.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(library)

    end = time.time()
    total_time = end - start
    print("\n"+ str(total_time))

# NOTE Currently no better than the dict that inits it, but I suspect I will be able to add useful methods.
# If not, I can always delete it, but I honestly like the syntax anyway.
class Book:
    def __init__(self, book):
        if not isinstance(book, dict):
            raise Exception("Tried to create a card with an improper input.")
        # Gather simple fields
        self.file = book['File Name']
        self.title = book['Title']
        self.author = book['Author']
        self.genre = book['Genre']

        # Gather sentence list from full text, then first and last sentences.
        script_dir = os.path.dirname(__file__)
        folder = 'Books'
        folder_path = os.path.join(script_dir, folder)
        selection = os.path.join(folder_path, book['File Name'])
        with open(selection) as f:
            contents = f.read()
        sents = sent_tokenize(contents)
        self.first = sents[(first := int(book['First Sentence']))]
        self.last = sents[(last := int(book['Last Sentence']))]
        self.split = sents[first:last]
        raw = [word_tokenize(sent, preserve_line=False) for sent in sents]
        self.words = [rem_punc(s) for s in raw]

def rem_punc(sent):
    allowed = set(ascii_letters+"'"+'-'+'_')
    new_list = []
    for word in sent:
        if allowed.issuperset(word):
            new_list.append(word)
    return new_list

def get_chars(sent):
    chars = 0
    for word in sent:
        chars += len(word)
    return chars


if __name__ == "__main__":
    main()