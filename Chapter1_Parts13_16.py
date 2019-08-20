# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 09:34:09 2019

@author: pjhal
"""

""" Chapter 1: Data Structures and Algorithms (Parts 13-16) """

#1.13 - Sorting a List of Dictionaries by a Common Key

#Problem: You have a list of dictionaries and you want to sort the entries according to one or more of the dictionary values
#Solution: Sorting this type of structure is easy using the operator module's itemgetter function. Let's say you've queried a database table for listing of people's info:

rows = [
    {'fname': 'Bob', 'lname': 'Dylan', 'uid': 1003},
    {'fname': 'Steve', 'lname': 'thePirate', 'uid': 1002},
    {'fname': 'Clyde', 'lname': 'Frog', 'uid': 1001},
    {'fname': 'Weston', 'lname': 'Dennis', 'uid': 1004},
    {'fname': 'Bob', 'lname': 'Marley', 'uid': 1005}
]

from operator import itemgetter

rows_by_fname = sorted(rows, key=itemgetter('fname'))
rows_by_uid = sorted(rows, key=itemgetter('uid'))

#print(rows_by_fname)
#print(rows_by_uid)

#itemgetter() function can also accdept multiple keys:
rows_by_flname = sorted(rows, key=itemgetter('fname', 'lname'))
#print(rows_by_flname)

#[rows] is passed to the built-in sorted() function, which accepts a key-word argument [key].
#This argument is expected to be a callable that accepts a single item from [rows] and returns a value that will be used as the basis for sorting.
#The itemgetter() function creates this callable.

#The operator.itemgetter() function takes (as arguments) the lookup indices used to extract desired values from records in [rows].
#It can be a dictionary key name, numeric list element, or any value that can be fed to an object's __getitem__() method.
#If you give multiple indices to itemgetter(), the callable it produces will return a tuple with all of the elements in it, and sorted() will order the output according to the sorted order of the tuples.

#The functionality of itemgetter() is sometimes replaced by [lambda] expressions:
rows_by_fname = sorted(rows, key=lambda r: r['fname'])
rows_by_flname = sorted(rows, key=lambda r: (r['fname'], r['lname']))

#This technique can also be applied to functions like min() and max()
min(rows, key=itemgetter('uid'))
max(rows, key=itemgetter('uid'))

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#1.14 - Sorting Objects Without Native Comparison Support

#Problem: You want to sort objects of the same class, but they don't natively support comparison operations
#Solution: The built-in sorted() function takes a key argument that can be passed a callable which will return some value in the object that sorted will use to compare objects.
#Say you have a sequence of User instances in your application, and you want to sort them by their user_id attribute, you supply a callable that takes a User instance as input and returns the user_id:

class User:
    def __init__(self, user_id):
        self.user_id = user_id
    def __repr__(self):
        return 'User({})'.format(self.user_id)
    
users = [User(21), User(5), User(94)]
sorted(users, key=lambda u: u.user_id)

#Instead of lambda, you can also use the operator.attrgetter():
from operator import attrgetter
sorted(users, key=attrgetter('user_id'))

#attrgetter() tends to be a bit faster and has added benefit of allowing multiple fields to be extracted simultaneously and can be used with functions like min() and max()
#note that this is analogous to using operator.itemgetter() for dictionaries (last section)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#1.15 - Grouping Records Together Based on a Field

#Problem: You have a sequence of dictionaries or instances and you want to iterate over the data in groups based on the value of a particular field (e.g. date)
#Solution: The itertools.groupby() function is useful for grouping data together in such a way. Suppose you have a list of dictionaries:

rows = [
    {'address': '4920 Nagle Ave.', 'date': '8/20/2019'},
    {'address': '1234 W Example', 'date': '8/23/2019'},
    {'address': '5923 S Coding', 'date': '8/20/2019'},
    {'address': '1616 Walnut', 'date': '8/21/2019'},
    {'address': '310 Beach Rd.', 'date': '8/29/2019'},
    {'address': '800 S Hanley', 'date': '8/21/2019'},
    {'address': '10203 Five Digit', 'date': '8/15/2019'},
    {'address': '8888 Gainsville', 'date': '8/21/2019'},
]

#If you wanted to iterate over the data in chunks grouped by date, first you have to sort by desired field then use itertools.groupby():

from operator import itemgetter
from itertools import groupby

rows.sort(key=itemgetter('date'))
#This sorts by the desired field first

for date, items in groupby(rows, key=itemgetter('date')):
    print(date)
    for i in items:
        print('    ', i)

#groupby() function works by scanning a sequence and finding sequential "runs" of identical values (or thoe returned by the given key function)
#On each iteration, it returns the value along with an iterator that produces all of the items in a group with the same value.
        
#Important preliminary step is to sort the data according to field of interest. Since groupby() only examines consecutive items, failing to sort first won't group records in desired fashion.
#If your goal is to group the data together by dates into a large data structure that allows random access, you might have better luck with defaultdict() to build a multidict (See: 1.6)
        
from collections import defaultdict
rows_by_date = defaultdict(list)
for row in rows:
    rows_by_date[row['date']].append(row)
    
#This allows for each date to be easily accessed via:
    
for r in rows_by_date['8/21/2019']:
    print(r)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#1.16 - Filtering Sequence Elements

#Problem: You have data inside of a sequence, and need to extract values or reduce the sequence using some criteria
#Solution: Easiest way to filter sequence data is often to just use a list comprehension:

alist = [1, 3, -4, 5, 10, -12, 2, -8, 7, -1]

[n for n in alist if n > 0]
[n for n in alist if n < 0]

#One downside to the list comprehension is that you might produce a large result if original input is also large.
#You can use generator expressions to produce filtered values iteratively:

pos = (n for n in alist if n > 0)

for x in pos:
    print(x)
    
#If the filtering criteria cannot be easily expressed in a list comprehension or generator expression (filtering involves exception handling) you can put filtering code into its own function and use filter():
blist = ['1', '2', '-3', '-', '4', 'N/A', '5']

def is_int(val):
    try:
        x = int(val)
        return True
    except ValueError:
        return False

ivals = list(filter(is_int, blist))
print(ivals)

#Since filter() creates an iterator, if you want to create a list of results, you must also use list() as shown

#List comprehensions and generator expressions are often the easiest and most straightforward ways to filter simple data. You can also use them to simultaneously transform the data:
import math
[math.sqrt(n) for n in alist if n > 0]

#A variation on filtering involves replacing values that don't meet the criteria with a new value instead of discarding them. Say you want to clip bad values to fit within a specified range:
clip_neg = [n if n > 0 else 0 for n in alist]
clip_pos = [n if n < 0 else 0 for n in alist]

#Another notable filtering tool is itertools.compress(), which takes an iterable and accompanying Boolean selector sequence as input. For the output, it gives you all of the items in the iterable where the corresponding element in the selector is True.
#This can be useful if you're trying to apply the results of filtering one sequence to another related one.

addresses = [
    '4920 Nagle Ave.',
    '1234 W Example',
    '5923 S Coding',
    '1616 Walnut',
    '310 Beach Rd.',
    '800 S Hanley',
]

counts = [3, 6, 0, 10, 4, 7]

#List of all addresses where corresponding count is greater than 5:
from itertools import compress
big5 = [n > 5 for n in counts]
list(compress(addresses, big5))

#The Boolean sequence indicates which elements satisfy the desired condition. The compress() function then picks out the items corresponding to True values.
#Like filter(), compress() normally returns an iterator. Therefore, you need to use list() to turn the results into a list if needed.