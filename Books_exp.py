#import ssl
#import nltk
import csv
import time
from nltk.corpus import gutenberg
from string import ascii_letters

#NOTE The below code was used to download what I needed from nltk
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context


def main():

    start = time.time()

    book_lib = []
    for fileid in gutenberg.fileids():
        if fileid == 'chesterton-ball.txt':
            continue
    #for fileid in ['melville-moby_dick.txt']:
        num_chars = len(gutenberg.raw(fileid))
        num_words = len(words := gutenberg.words(fileid))
        num_sents = len(sents := gutenberg.sents(fileid))
        num_paras = len(paras := gutenberg.paras(fileid))
        # get total vocabulary used in this book
        num_vocab = len(set(w.lower() for w in words))
        if fileid in ['shakespeare-caesar.txt', 'shakespeare-hamlet.txt', 'shakespeare-macbeth.txt']:
            last = sents[len(sents)-5]
            final = paras[len(paras)-3]
        elif fileid in ['austen-emma.txt', 'austen-persuasion.txt', 'austen-sense.txt', 'milton-paradise.txt']:
            last = sents[len(sents)-2]
            final = paras[len(paras)-2]
        else:
            last = sents[len(sents)-1]
            final = paras[len(paras)-1]

        # Checks each "word" in the last sentence and records the number of character, ignoring punctuation
        ls_chars = char_count(last)
        lp_chars = []
        lp_words = 0
        lp_read = ""
        for sent in final:
            lp_chars.extend(char_count(sent))
            lp_words += len(sent)
            if lp_read == "":
                lp_read = readable(sent)
            else:
                lp_read += " " + readable(sent)

        book_lib.append({
            'author-book': fileid.split('.')[0] # remove .txt from file name
            ,'total_characters': num_chars
            ,'total_words': num_words    
            ,'total_sentences': num_sents
            ,'total_paragraphs': num_paras
            # total vocabulary used divide total words used
            ,'total_vocabulary': num_vocab
            ,'vocabulary_rate':round(num_vocab/num_words,2) 
            ,'ls_characters': sum(ls_chars)
            ,'ls_words':len(last)
            ,'last_sentence': readable(last)
            ,'lp_characters': sum(lp_chars)
            ,'lp_words': lp_words
            ,'lp_sentences': len(final)
            ,'last_paragraph': lp_read
        })

    keys = book_lib[0].keys()
    with open('books_last.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(book_lib)

    end = time.time()
    total_time = end - start
    print("\n"+ str(total_time))


def readable(last):
    allowed = set(ascii_letters+"'")
    sent = ""
    for i in range(0, len(last)):
        if i == 0 or not allowed.issuperset(last[i]) or last[i-1] == '-':
            sent = sent + last[i]
        else:
            sent = sent + " " + last[i]
    return sent

def char_count(last):
    lst = []
    for word in last:
        # if allowed.issuperset(word):
        #     if "'" in word:
        #         lst.append(len(word)-1)
        #     else:
        #         lst.append(len(word))
        lst.append(len(word))
    return lst

if __name__ == "__main__":
    main()