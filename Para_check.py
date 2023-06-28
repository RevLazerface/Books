import nltk.corpus
import os

def main():
    print("Choose from the following file names:\n")
    script_dir = os.path.dirname(__file__)
    subs = "Books"
    path = os.path.join(script_dir, subs)
    
    books = os.listdir(path)
    x = 0
    for book in books:
        print(f"{x}: {book}")
        x += 1
    choice = input("Book index number: ")
    

if __name__ == "__main__":
    main()