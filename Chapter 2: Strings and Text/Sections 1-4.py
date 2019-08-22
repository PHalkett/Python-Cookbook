# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 16:14:11 2019

@author: pjhal
"""

""" Chapter 2: Strings and Text (Parts 1-) """

#2.1 - Splitting Strings on Any of Multiple Delimiters

#Problem: You need to split a string into fields, but the delimiters (and spacing around them) aren't consistent throughout the string
#Solution: The split() method of string objects is meant for simple cases, does not allow for delimiters or account for possible whitespace around delimiters
#For cases where you need some more flexibility, we use the re.split() method:

line = 'asdfaae aspdoifqd; poiqwe, aspdofiqw,       fool'
import re 
re.split(r'[;,\s]\s*', line)

#The re.split() function is useful because we can specify multiple patterns for the separator(s) [comma, semicolon, whitespace, etc.]
#Whenever that pattern is found, the entire match becomes the delimiter between whatever fields lie on either side of the match. The result here is a list of fields, just as we'd have with str.split()
#You need to be a bit careful when using re.split() because should the regular expression/pattern involve a capture group enclosed in parenthesis they will also be included in the result

#This is an example of where we include each of the delimiters as well
fields = re.split(r'(;|,|\s)\s*', line)
#print(fields)

#Getting the split characters could be useful, maybe you need them later on to reform some output string:
values = fields[::2]
delimiters = fields[1::2] + ['']
#print(values)
#print(delimiters)

#If you don't want the separator characters in the result, but you still need to use parenthesis to group parts of the regular expression pattern, make sure you use noncapture group specified as (?:...)
re.split(r'(?:,|;|\s)\s*', line)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#2.2 - Matching Text at the Start or End of a String

#Problem: You need to check the start or end of a string for some specific text pattern, such as a filename, extension, URL, etc.
#Solution: If you want to check the beginning of the string we can use str.startswith() method and if we want to check the end we can use str.endswith() method:

filename = 'something.txt'

#filename.endswith('.txt') would return True
#filename.startswith('file:') would return False

url = 'http://www.python.org'
url.startswith('http:')

#If you need to check against multiple choices, simply provide a tuple of possibilities to startswith() and endswith():
import os
filenames = os.listdir('.')
[name for name in filenames if name.endswith(('.c', '.py'))]

from urllib.request import urlopen

def read_data(name):
    if name.startswith(('http:', 'https:', 'ftp:')):
        return urlopen(name).read()
    else:
        with open(name) as f:
            return f.read()
        
#This is one part of Python where a tuple is actually REQUIRED as an input. If you happen to have the choices specified in a list/set, just convert them using tuple() first:
choices = ['http:', 'ftp:']
url = 'http://www.python.org'
#url.startswith(choices) will throw a TypeError
url.startswith(tuple(choices))

#The startswith() and endswith() methods provide a convenient way to perform basic prefix/suffix checking. Similar operations can be done with slice, but it's not as ... clear:
filename = ('something.txt')
filename[-4:] == '.txt'

url = 'http://www.python.org'
url[:5] == 'http:' or url[:6] == 'https:' or url[:4] == 'ftp:'

#You could even use a regular expression as an alternative, but this can be overkill:
import re
url = 'http://www.python.org'
re.match('http:|https:|ftp:', url)

#Lastly, startswith() and endswith() methods work well when combined with some other operators, such as common data reductions.
#For example, we could use this statement to check a directory for the presence of some type of file:

#if any(name.endswith(('.txt', '.py')) for name in listdir(dirname)):
    

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
#2.3 - Matching Strings Using Shell Wildcard Patterns

#Problem: You want to match text string using the same wildcard patterns that are commonly used when working in Unix shells (*.py, Dat[0-9]*.csv, etc.)
#Solution: You [fnmatch] provides two functions-- fnmatch() and fnmatchcase() -- that can be used to perform such a matching, usage is simple:
    
from fnmatch import fnmatch, fnmatchcase

fnmatch('foo.txt', '*.txt')
fnmatch('foo.txt', '?oo.txt')
fnmatch('Dat45.csv', 'Dat[0-9]*')

names = ['Dat1.csv', 'Dat2.csv', 'config.ini', 'program.py']
[name for name in names if fnmatch(name, 'Dat*.csv')]

#Normally, fnmatch() matches our patterns using the same case-sensitivity rules as the system's underlying filesystem (varies based on your OS)
#On Mac OS X
#fnmatch('example.txt', '*.TXT') this would return a FALSE

#On Windows
#fnmatch('example.txt', '*.TXT') this would return a TRUE

#Another features of this function is that their potential use with data processing of nonfilename strings:
addresses = [
    '6969 N Bone St',
    '420 S Yolo Rd',
    '12 W AllFollows Blvd.',
    '12345 E Example Ave'
]

#You could make a list comprehension like so:
[addr for addr in addresses if fnmatchcase(addr, '* Rd')]
[addr for addr in addresses if fnmatchcase(addr, '123[0-9][0-9] *Example*')]

#The matching performed by fnmatch somewhere between functionality of simple string methods and full power regular expression.
#If you're trying to provide some simple mechanism for allowing wildcards in data processing operations, it's a useful/reasonable solution.

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#2.4 - Matching and Searching for Text Patterns

#Problem: You want to match or search text for a specific pattern
#Solution: If the text you're trying to match is a literal, you can usually just use the basic string methods, like str.find(), str.endswith(), str.startswith(), etc.

text = 'where are all of my friends at, yo'

#If we want an exact match
text == 'where'

#Match at the start or the end
text.startswith('are')
text.endswith('yo')

#Search for the location of the first occurrence
text.find('of')

#For complicated matching, we can use regular expressionsd and the [re] module. If we want to show the basic mechanics of using regular expressions, say you wanted to match dates specified as digits:
text1 = '8/22/2019'
text2 = 'August 22, 2019'

import re

#Simple matching: \d+ means match one or more digits
'''
if re.match(r'\d+/\d+/\d+', text1):
    print('yes')
else:
    print('no')
    
if re.match(r'\d+/\d+/\d+', text2):
    print('yes')
else:
    print('no')
'''
    
#If you're going to perform a lot of matches using the same pattern, it usually helps to precompile the regular expressions pattern into a pattern object first:
datepat = re.compile(r'\d+/\d+/\d+')
if datepat.match(text1):
    print('yes')
else:
    print('no')
    
if datepat.match(text2):
    print('yes')
else:
    print('no')

#So match() always tries to find the match at the start of the string. If you wanted to search text for ALL occurrences of a pattern, use the findall() method:
text = 'Today is 8/22/2019. TwitchCon starts on 9/27/2019.'
datepat.findall(text)

#When we're defining regular expressions, it's common to use capture groups by enclosing parts of the pattern in parenthesis:
datepat = re.compile(r'(\d+)/(\d+)/(\d+)')

#Capture groups simplify subsequent processing of the matched text because contents of each group can be extracted individually:
m = datepat.match('8/22/2019')

#Extract contents of each group
#Gives entire date
m.group(0)

#Gives the month
m.group(1)

#Gives the day
m.group(2)

#Find all matches (notice the splitting into tuples)
datepat.findall(text)

month, day, year = m.groups()
for month, day, year in datepat.findall(text):
    print('{}-{}-{}'.format(year, month, day))
    
#The findall() method searches the text and finds ... all matches, returning them as a list.
#If you wanted to find matches iteratively, use finditer() method instead:

for m in datepat.finditer(text):
    print(m.groups())
    
#The essential functionality here is first compiling a pattern using re.compile() and then using methods such as match(), findall(), and finditer() 
#When specifying patterns, it is common to use raw strings like r'(\d+)/(\d+)/(\d+)'. These strings leave backslash uninterpreted, which can be useful for regular expressions
#Otherwise, you need to use double backslash

#Keep in mind that the match() method only checks the beginning of a string, can match things you aren't expecting.
#If you want an exact match, just make sure the pattern includes the end-marker ($):
datepat = re.compile(r'(\d+)/(\d+)/(\d+)$')
datepat.match('8/22/2019asbasdfe')
datepat.match('8/22/2019')

#If you're just doing a simple text matching/searching operation, you can often skip the compilation step and use module-level functions in the re module instead:
re.findall(r'(\d+)/(\d+)/(\d+)', text)

#If you're going to perform a lot of matching or searching, it is often beneficial to compile the pattern first and use it over and over again.
#The module-level functions keep a cache of recently compiled patterns, so there isn't much of a performance reduction, you'll save a few lookups/extra processing