# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 13:05:11 2019

@author: pjhal
"""

""" Chapter 1: Data Structures and Algorithms (Parts 17-20) """

#1.17 - Extracting a Subset of a Dictionary

#Problem: You want to make a dictionary that is a subset of another dictionary
#Solution: This can be done easily using a dictionary comprehension:

prices = {
    'AMD': 45.45,
    'INTEL': 333.33,
    'TSLA': 250.50,
    'NTDOY': 40.40,
    'FB': 25.25
}

#Create a dictionary of all prices over 200
p1 = {key:value for key, value in prices.items() if value > 200}

#Create a dictionary of all tech stocks
tech_names = {'AMD', 'INTEL', 'TSLA'}
p2 = {key:value for key, value in prices.items() if key in tech_names}

#What dictionary comprehension does can also be accomplished with a sequence of tuples and passing them to dict() function:
p1 = dict((key, value) for key, value in prices.items() if value > 200)

#However, dictionary comprehension solution is often clearer and can run almost twice as quickly
#The second example could also be done with the (somewhat slower) method:
p2 = {key:prices[key] for key in prices.keys() & tech_names}

#See Section 14.13 for information about timing/profiling

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#1.18 - Mapping Names to Sequence Elements

#Problem - You have code that accesses list or tuple elements by position, but it can be difficult to read at times. 
#You want to be less dependent on position in structure by accessing elements by name.

#Solution - [collections.namedtuple()] can provide these benefits, while also adding minimal overhead over a normal tuple object.
#It is actually a factory method that returns a subclass of the standard Python tuple type. Give it a type, name, fields, and it returns a class that you can instantiate, pass in values, etc.

from collections import namedtuple
Subscriber = namedtuple('Subscriber', ['addr', 'joined'])
sub = Subscriber('bob@example.com', '2019-8-8')
Subscriber(addr='bob@example.com', joined='2019-8-8')

#print(sub.addr)
#print(sub.joined)

#A major use case for named tuples is decoupling your code from the position of the elements it manipulates.
#If you get back a large list of tuples from a database call, then manipulate them by accessing positional elements, code could break if you did something like add a new column to the table.
#This is not the case if you first cast the returned tuples to namedtuples

def compute_cost(records):
    total = 0.0
    for rec in records:
        total += rec[1] * rec[2]
    return total

from collections import namedtuple

Stock = namedtuple('Stock', ['name', 'shares', 'price'])

def compute_cost(records):
    total = 0.0
    for rec in records:
        s = Stock(*rec)
        total += s.shares * s.price
    return total

from collections import namedtuple

Stock = namedtuple('Stock', ['name', 'shares', 'price'])

def compute_cost(records):
    total = 0.0
    for rec in records:
        s = Stock(*rec)
        total += s.shares * s.price
    return total

#One use of the [namedtuple] is as a replacement for a dictionary, which requires more space to store
#If you're building a large data structure involving dictionaries, using [namedtuple] will be more efficient
#Keep in mind: unlike a dictionary, a [namedtupe] is immutable
    
s = Stock('AMD', 100, 45.45)
#this will throw error: s.shares = 75

#If you needed to change any of the attributes, it could be done using the _replace() method of a namedtuple instance, which would make an entirely new namedtuple with specified values replaced
#s = s._replace(shares=75)
    
#Another use of the _replace() method is that it can be used to populate named tuples that have optional or missing fields.
#You'd make a prototype tuple which contains default values and then use _replace to create new instances with replaced values.

from collections import namedtuple

Stock = namedtuple('Stock', ['name', 'shares', 'price', 'date', 'time'])

#Create a prototype instance
stock_proto = Stock('', 0, 0.0, None, None)

#Converting function from dictionary to Stock
def dict_to_stock(s):
    return stock_proto._replace(**s)

#If your goal is to define an efficient data structure where you will change various instance attributes, using [namedtuple] is not the best choice.
#Consider defining a class using __slots__ instead (see Section 8.4)
    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
#1.19 -Transforming and Reducing Data at the Same Time
    
#Problem: You want to execute a reduction function (sum(), min(), max()), but first you need to filter or transform the data
#Solution: We could use a generator-expression argument in order to combine and reduce the data simultaneously

numbers = [1, 2, 3, 4, 5]
s = sum(x * x for x in numbers)

import os
files = os.listdir('C:\Coding Folder\Spyder Files\Chapter 1')
#files = os.listdir('C:\Coding Folder\R Files\statshw\ACD')
'''
if any(name.endswith('.py') for name in files):
    print('There be python!')
else:
    print('Sorry, no python.')
'''
#Output as CSV
s = ('AMD', 50, 45.45)
#print(','.join(str(x) for x in s))

#Data reduction across fields of a data structure:
portfolio = [
    {'name': 'AMD', 'shares': 50},
    {'name': 'TSLA', 'shares': 20},
    {'name': 'NTDOY', 'shares': 100},
    {'name': 'FB', 'shares': 20},
    {'name': 'APHR', 'shares': 1000},
]

min_shares = min(s['shares'] for s in portfolio)

#Subtle syntactic aspect of a generator expression when supplied as the single argument to a function (you don't need repeated parenthesis)
#Using a generator argument is more efficient than first creating some temporary list. If you didn't use a generator expression, you could do something like:

numbers = [1, 2, 3, 4, 5]
s = sum([x * x for x in numbers])

#This introduces an extra step. For such a small list, not much of a difference. If we were working with huge amount of numbers, we'd make a giant temporary data structure, which would be used once then discarded.
#The generator solution transforms our data iteratively and is therefore much more memory-efficient

#Certain reduction functions like min() and max() which accept a key argument that might be useful in situations where you'd be inclined to use a generator, consider the alternative:

min_shares = min(s['shares'] for s in portfolio)

min_shares = min(portfolio, key=lambda s: s['shares'])

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#1.20 - Combining Multiple Mappings into a Single Mapping

#Problem: You have multiple dictionaries or mappings that you want to combine into a single mapping to perform certain operations, like looking up values or checking for the existence of keys
#Solution: Start with Two Dictionaries:

a = {'x': 1, 'z': 2}
b = {'w': 3, 'z': 4}

#Let's say you wanted to perform lookups where you check both dictionaries (first check a then b if not found).
#One way of doing this would be to use the [ChainMap] class from collections module like so:

from collections import ChainMap
c = ChainMap(a,b)
#print(c['x'])

#ChainMap takes multiple mappings and makes them appear logically as one. Let's say that the mappings are not literally merged together.
#Instead, ChainMap keeps all of our underlying mappings and redefines a common dictionary operation to scan the list:

#print(len(c))
#print(list(c.keys()))
#print(list(c.values()))

#If there are duplicate keys, the values from our first mapping get used. Therefore, the entry c['z'] would always refer to the value in dictionary a, not in b.
#ChainMaps are particularly useful when working with scoped values ... such as variables in a language (globals, locals, etc.). There are methods that make this easy:

values = ChainMap()
values['x'] = 1

#Add a new mapping
values = values.new_child()
values['x'] = 2

values = values.new_child()
values['x'] = 3

#print(values)

#Discard last mapping
values = values.parents
#print(values['x'])

#An alternative to ChainMap, you could merge dictionaries together using the update() method:
merged = dict(b)
merged.update(a)

#This works, but it requires you make a completely separate dictionary object (this destroys another).
#Also, if any of the original dictionaries mutate, the changes don't get reflected in the merged dictionary


print(merged['x'])

#ChainMap uses the ORIGINAL dictionaries, so it doesn't have this behavior:
a = {'x': 1, 'z': 3}
b = {'y': 2, 'z': 69}

merged = ChainMap(a,b)
a['x'] = 12

