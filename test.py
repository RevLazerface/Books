from nltk.tokenize import sent_tokenize, word_tokenize

def main():
    x = input("")
    if x.isnumeric():
        print("True")
    else:
        print("False")
    # full = "this has a bunch of chars.  this does too"
    # sents = word_tokenize(full, preserve_line=True)
    # words = word_tokenize(full, preserve_line=False)
    # print(sents)
    # print(words)

def get_chars(sent):
    chars = 0
    for word in sent:
        chars += len(word)
    return chars

if __name__ == "__main__":
    main()