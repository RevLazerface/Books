from nltk.corpus import gutenberg
from string import ascii_letters
from Books_exp import readable

# whit = gutenberg.paras('whitman-leaves.txt')
# last = whit[len(whit)-1]
# final = ""
# for sent in last:
#     final = final + " " + readable(sent)
# print("\n\n")
# print(len(last))
# print(final)
# print("\n\n")

for work in ['bryant-stories.txt']:
    shaq = gutenberg.paras(work)
    final = shaq[0]
    para_read = ""
    for sent in final:
        if para_read == "":
            para_read = readable(sent)
        else:
            para_read += " " + readable(sent)
    print(f"\n{para_read}\n")

#print(gutenberg.fileids())