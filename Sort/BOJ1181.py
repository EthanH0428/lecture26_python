import sys

n = int(sys.stdin.readline())

words = set()
for _ in range(n):
    words.add(sys.stdin.readline().strip()) 

word_list = list(words)

word_list.sort(key=lambda x: (len(x), x))

for word in word_list:
    print(word)