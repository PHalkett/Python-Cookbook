# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 10:08:35 2019

@author: pjhal
"""

""" Chapter 2: Strings and Text (Parts 13-16) """

#2.13 - Aligning Text Strings

#Problem: You need to format text with some sort of alignment applied.
#Solution: For basic alignment of strings, the ljust(), rjust(), and center() methods of strings can be used:
text = 'Hello World'
text.ljust(20) #will give Hello World on the LHS of a 20 character long string, whitespace at the end
text.rjust(20) #will give Hello World on the RHS of a 20 character long string, whitespace at the front
text.center(20) #will give Hello World in the center of a 20 character long string, whitespace even on both sides

#All of these methods also accept an optional fill character as well:
text.center(20, '*') #will give Hello World in the center of a 20 character long string, with * evenly on both sides

#The format() function can also be used to easily align things, you just need to use the <, >, or ^ characters along with desired width:
format(text, '>20')  #same as rjust
format(text, '<20')  #same as ljust
format(text, '^20')  #same as center

#If you want to include a fill character other than space, specify before alignment character:
format(text, '=^20s') #same as center *

#These format codes can also be used in the format() method when formatting multiple values:
'{:>10s}{:>10s}'.format('Hello', 'World')

#One benefit of format() is that it is not specific to strings. It will work with any value, making it more general purpose, numbers for example:
x = 1.2345
format(x, '>10') #Aligns our value on the right side of 10 spaces
format(x, '^10.2f') #This will cutoff our value at the hundreths digit and also center it

#In older code you will also see the % operator used to format text. But in new code you should usually prefer the format() method.
#It is more powerful than the % operator and is more general purpose than ljust(), rjust(), and center() methods.

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#2.14 - Combining and Concatenating Strings

#Problem: You want to combine many small strings together into a larger string.
#Solution: If the strings you wish to combine are found in a sequence or iterable, the fastest way is to use the join() method:
parts = ['What', 'Is', 'Love', '?']
' '.join(parts)
','.join(parts)
''.join(parts)

#join() operation is specified as a method on strings because the objects you want to join could come from any number of different data sequences (lists, tuples, dicts, files, sets, generators)
#If you're only combining a few, you can usually just use + like so:
a = "Baby Don't"
b = 'Hurt Me'
a + ' ' + b

#This also works as a substitute for more complicated formatting operations:
print('{} {}'.format(a,b))
print(a + ' ' + b)

#If you're combining literals together in source code, you may just place them next to each other with out the + operator:
a = 'One' 'Two'
a #will return OneTwo

#Joining strings is often an area where programmers make choices that severely impact the performance of the code.
#The most important thing to keep in mind is that using the + operator to join a lot of strings is extremely inefficient due to the memory copies and garbage collection that occurs.
#One trick is conversion of data to strings and concatentation at the same time using a generator expression (See Section 1.19):
data = ['NTDOY', 100, 45.5]
','.join(str(d) for d in data) #Thiswill return the values separated by commas

#Sometimes programmers make unnecessary string concatenations that are more complicated than needed:
c = 'Three' 'Four'
print(a + ':' + b + ':' + c) #not good
print(':'.join([a, b, c])) #still not optimal
print(a, b, c, sep=':') #cleaner/faster

#Mixing I/O operations and string concatenation is something that has varied uses and applications, consider fragments:
f = open('example.txt', 'w')
chunk1 = 'chunk1'
chunk2 = 'chunk2'

f.write(chunk1 + chunk2) #V1 with string concatenation

f.write(chunk1) #V2 with separate I/O ops)
f.write(chunk2)

#If the two strings are small, then the first version might offer better performance due to inherent expense of carrying out I/O system call.
#If the two strings are large, the second version might be more efficient since it avoids making large temporary result and copying large blocks of memory ground.
#If you're writing code that is building output from lots of small strings, consider writing it as a generator function, using yield to emit fragments:
def sample():
    yield 'What'
    yield 'Is'
    yield 'Love'
    yield '?'

#This approach makes no assumption about how the fragments are to be assembled together, you could use:
text = ''.join(sample())

#Or redirect fragments to I/O:
for part in sample():
    f.write(part)

#Or you could make hybrid that combines I/O operations in an intelligent manner:
def combine(source, maxsize):
    parts = []
    size = 0
    for part in source:
        parts.append(part)
        size += len(part)
        if size > maxsize:
            yield ''.join(parts)
            parts = []
            size = 0
        yield ''.join(parts)

for part in combine(sample, 32768):
    f.write(part)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#2.15 - Interpolating Variables in Strings
    
#Problem: You want to create a string in which embedded variable names are substituted with a string representation of a variable's value.
#Solution: Python has no direct support for simply substituting variable values in strings. This feature can be approx. using the format() method:
s = '{name} has {n} messages.'
s.format(name='Vader', n=66) #Will return 'Vader has 66 messages.'

#If the values to be substituted are truly found in variables, you can use the combination of format_map() and vars():
name = 'Vader'
n = 66
s.format_map(vars()) #Will return the same as above.

#One downside of format() and format_map() is that they do not work well with missing values, will throw a 'KeyError'
#A method for avoiding this issue is to define an alternative dictionary class with a __missing__() method, as such:
class safesub(dict):
    def __missing__(self, key):
        return '{' + key + '}'

#Now use this class to wrap the inputs to format_map():
del n #Make sure n is undefined
s.format_map(safesub(vars())) #Will return 'Vader has {n} messages.'

#If you find yourself frequently performing these steps, you could hide variable substitution process behind utility function which employs a "frame hack":
import sys
def sub(text):
    return text.format_map(safesub(sys._getframe(1).f_locals))

#This will allow you to type things like:
name = 'Vader'
n = 66
print(sub('Hello {name}'))
print(sub('You have {n} messages.'))
print(sub('Your favorite color is {color}'))

#The lack of true variable interpolation in Python has led to a number of alternatives/work-arounds. An alternative to the methods aforementioned is to sometimes format strings like so:
name = 'Vader'
n = 66
'%(name) has %(n) messages' %vars()

#Or a template of strings:
import string
s = string.Template('$name has $n messages.')
s.substitute(vars())

#The format() and format_map() methods are more modern though and should be preferred in most cases. 
#One benefit of the format() is that you also get all features related to string formatting (alignment, padding, numerical formatting, etc.) which is not possible with something like the Template string object alternative.

#There are a number of other interesting features illustrated from these examples. The __missing()__ method of mapping/dict classes is a method that you can define to handle missing values.
#In the safesub class, this method has been defined to return missing values back as a placeholder. Instead of throwing a KeyError exception, you would see the missing values appearing in the resulting string (potentially useful for debugging).

#The sub() function uses sys._getframe(1) to return stack frame of the caller. From there, the f_locals attribute is accessed to get the local variables (messing with stack frames should be avoided in most coding situations).
#f_locals is a dictionary that is a copy of the local variables in the calling function. Although you can modify contents of f_locals, it does not have any lasting effect. 
#Even though accessing diff stack frame looks dangerous, its not possible to overwrite variables or change local environment of the caller.

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#2.16 - Reformatting Text to a Fixed Number of Columns

#Problem: You have long strings that you want to reform so that they fill a user-specified number of columns.
#Solution: Use the textwrap module to reformat text for output:
s = "There once was a man from Peru, \
who dreamed he was eating a shoe, \
he woke with a fright in the middle of the night \
to find that his dream had come true"

import textwrap
print(textwrap.fill(s, 70))
print(textwrap.fill(s, 40))
print(textwrap.fill(s, 40, initial_indent='    ')) #Adds a tab in the front
print(textwrap.fill(s, 40, subsequent_indent='    ')) #Adds a tab to every line after

#textwrap module is a straightforward way to clean up text for printing - especially if you want the output to fit nicely on the terminal.
#You can also obtain terminal size with:
import os
os.get_terminal_size().columns

#fill() method also has some additional options that control how it handles tabs, sentence endings, etc.