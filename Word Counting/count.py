import re

BOOK = "birds.txt"

with open(BOOK) as f:
    text = f.read()
f.closed

words = re.split(r'[\W\s]', text)

count = {}
for word in words:
    word = word.lower()
    if word not in count:
        count[word] = 0
    count[word] += 1

print count
