# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 14:14:51 2019

@author: pjhal
"""

""" Chapter 1: Data Structures and Algorithms (Parts 9-12) """

#1.9 - Finding Commonalities in Two Dictionaries

#Problem: You have two dictionaries and want to find out what they have in common (keys, values, etc.)
#Solution: To find out what the two dictionaries have in common, simply use the set operations keys() or items():

a = {
   'x' : 1,
   'y' : 2,
   'z' : 3
}

b = {
   'w' : 10,
   'x' : 11,
   'y' : 2
}

#Find keys in common
a.keys() & b.keys()

#Find keys in 'a' that are not in 'b'
a.keys() - b.keys()

#Find (key,value) pairs in common
a.items() & b.items()

#These operations can also be used to alter or filter dictionary contents:
c = {key:a[key] for key in a.keys() - {'z', 'w'}}

#A dictionary is a mapping between keys and values. The keys() method of a dictionary returns a key-view object that exposes keys.
#Keys view also supports common set operations such as unions, intersections, and differences.
#If you need to perform common set operations with dictionary keys, you can often use keys-view objects directly w/o converting into a set.

#The items() method returns an items-view object consisting of (key,value) pairs. Object supports similar set operations and can be used to perform operations such as finding key-value pair in two dictionaries.
#The values() method of a dictionary does not support set operations since, unlike keys, items contained in a value view isn't guaranteed to be unique (you can simply convert values into a set first)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#1.10 - Removing Duplicates from a Sequence while Maintaining Order

#Problem: You want to eliminate the duplicate values in a sequence, but preserve the order of the remaining items
#Solution: If the values are hashable, problem can be solved easily with a set and generator:

def dedupe(items):
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)
            
#Provide sequence:
a = [1, 2, 3, 5, 4, 3, 1, 10, 5, 1, 12]
#print(list(dedupe((a))))

#Solution2: If the values are not hashable (dicts), you ocan make a slight change to the above:

def dedupe2(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if item not in seen:
            yield item
            seen.add(val)

#The purpose of the key argument is to specify a function that converts sequence items into a hashable type for the purpose of duplicate detection:
            
a2 = [{'x':1, 'y':2}, {'x':1, 'y':3}, {'x':1, 'y':2}, {'x':1, 'y':4}]
#print(list(dedupe(a, key=lambda d: (d['x'],d['y']))))
#print(list(dedupe(a, key=lambda d: d['x'])))

#This solution works well if you want to eliminate duplicates based on the value of a single field or attribute or a larger data structure.

#If all you want to do is eliminate duplicates, you can often just make a set. However, this does not preserve any kind of ordering, so the data will be scrambled.
#The use of a generator function reflects the fact that you might want the function to be general purpose - not necessarily tied to list processing
#If you wanted to read a file and eliminiate duplicate lines, you could try:

with open('somefile.txt', 'r') as f:
    for line in dedupe(f):
        print(line)
        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
#1.11 - Naming a Slice

#Problem: Your program has become an unreadable mess of hardcoded slice indices and you want to clean it up:
#Solution: If you have code pulling specific data fields out of a record string with fixed fields (flat file, etc.):

'01235678901234567890123456578900123567890123456789012345657890'

record = '...........100        ........513.25      ...........'
cost = int(record[20:32]) * float(record[40:48])
#print(cost)

#Instead, name the slices for easier manipulation:

SHARES = slice(20,32)
PRICE = slice(40,48)

cost = int(record[SHARES]) * float(record[PRICE])
#print(cost)

#In general coding practice, writing with a lot of hardcoded index values leads to readability/maintenance issues.
#The built in slice() creates an object that can be used anywhere a slice is allowed:

items = [0, 1, 2, 3, 4, 5, 6]
a = slice(2, 4)
#items[2:4] will be the same as item[a]

items[a] = [10,11]
#this will replace 2, 3 with 10, 11 in our list

del items[a]
#this will remove 10, 11 from our list

#If you have a slice instance s, you can get more info about it by looking at its s.start, s.stop, and s.step attributes:
a = slice(5, 50, 2)
#print(a.start)
#print(a.stop)
#print(a.step)

#You can map a slice onto a sequence of a specific size by using indices(size). This will return a tuple (start, stop, step) where all values have been suitably limited to fit within bounds:
s = 'HelloWorld'
a.indices(len(s))
for i in range(*a.indices(len(s))):
    print(s[i])

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#1.12 - Determining the Most Frequently Occurring Items in a Sequence

#Problem: You have a sequence of items, and you'd like to determine the most frequently occurring items in the sequence
#Solution: The collections.Counter class is designed for this type of problem. It comes with a useful most_common() method that will give you the answer:
    
words = [
    'once', 'twice', 'thrice', 'once', 'twice', 'chicken', 'noodle', 'soup', 'with', 'rice', 'once', 'twice', "don't", 'forget', 'the', 'ice'
]

from collections import Counter
word_counts = Counter(words)
top_three = word_counts.most_common(3)
print(top_three)

#If you do not have enough multiples to fulfill the top three, it will use the first in the list

#Counter objects can be fed any sequence of hashable input items. Counter is a dictionary that maps the items to the number of occurrences:
word_counts['once']

#If you wanted to increment the count manually, just use addition:
morewords = ['once', 'twice', 'three', 'times', 'a', 'lady']
for word in morewords:
    word_counts[word] += 1

#Alternatively, you could use the update() method:
word_counts.update(morewords)

#A little-known feature of Counter instances is that they can be easily combined with various mathematical operations:
a = Counter(words)
b = Counter(morewords)

#Combine counts
c = a + b

#Subtract counts
d = a - b

#Counter objects are extremely useful for most kinds of problems involving data counting and tabulation. You should use this over manually written solutions involving dictionaries. 