# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 15:21:08 2019

@author: pjhal
"""

""" Chapter 2: Strings and Text (Parts 9-12) """

#2.9 - Normalizing Unicode Text to a Standard Representation

#Problem: You're working with Unicode strings, but need to make sure that all of the strings have the same underlying representation
#Solution: In Unicode, certain characters can be represented by more than one sequence of code points:
s1 = 'Spicy Jalape\u00f1o'
s2 = 'Spicy Jalapen\u0303o'

#s1 == s2 will return False as their lengths are different

#Having multiple representations is a problem for programs that compare strings. In order to fix this, you should normalize text into standard representation using [unicodedata]:
import unicodedata
t1 = unicodedata.normalize('NFC', s1)
t2 = unicodedata.normalize('NFC', s2)
#t1 == t2 will return True
print(ascii(t1))

t3 = unicodedata.normalize('NFD', s1)
t4 = unicodedata.normalize('NFD', s2)
#t3 == t4 will also return True
print(ascii(t3))

#The first argument to normalize() specifies how you want the string normalized. NFC means that characters should be fully composed (use single code point if possible)
#NFD means that characters should be fully decomposed with use of combining characters.

#Python supports normalization forms NFKC and NFKD, which add extra compatibility features for dealing with certain kinds of characters:
s = '\ufb01'
unicodedata.normalize('NFD', s)
#Both of these will return 'fi'

#You can break apart the combined letters with:
unicodedata.normalize('NFKD', s)
unicodedata.normalize('NFKC', s)
#Both of these will return 'fi' but separated

#Normalization is a part of any code that needs to ensure that it processes Unicode text in a consistent/logical manner. This is especially true when it processes strings received as part of user input.
#Normalization can also be important when sanitizing/filtering text. Say you want to remove diacritical marks from text:
t1 = unicodedata.normalize('NFD', s1)
''.join(c for c in t1 if not unicodedata.combining(c))

#This shows how the unicodedata module utility functions help test characters against character class. The combining() function tests a character to see if it is a combining character.
#There are other functions in the module for finding character categories, testing digits, etc.

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#2.10 - Working with Unicode Characters in Regular Expressions

#Problem: You are using regular expressions to process text, but are concerned about the handling of Unicode characters.
#Solution: By default, the re module is already programmed with rudimentary knowledge of certain Unicode character classes:
import re
num = re.compile('\d+')
#ASCII digits
num.match('123')

#Arabic digits
num.match('\u0661\u0662\u0663')

#If you need to include specific Unicode characters in patterns, you can use the usual escape sequence for Unicode characters (\uFFFF or \UFFFFFF)

#When performing matching/searching operations, it's a good idea to normalize and possibly sanitize all text to a standard form first (see Section 2.9).
#Be aware of special case-insensitive matching combined with case folding:
pat = re.compile('stra\u00dfe', re.IGNORECASE)
s = 'straße'
pat.match(s)
pat.match(s.upper())
s.upper()

#Mixing Unicode and regular expressions is extremely confusing. Consider installing [regex] library if you want to do it seriously.

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#2.11 - Stripping Unwanted Characters from Strings

#Problem: You want to strip unwanted characters (such as a whitespace) from the beginning, middle, or end of a text string.
#Solution: The strip() method can be used to strip characters from the beginning or end of a string. lstrip() and rstrip() will perform from left or right side, by default they strip whitespace but can be given other characters.
s = '      hello world     \n'
s.strip()
s.lstrip()
s.rstrip()

t = '-------hello======'
t.lstrip('-')
t.strip('-=')

#The various strip() methods are commonly used when reading and cleaning up data for processing. You can use them to get rid of whitespace, remove quotations, etc.
#Stripping does not apply to any text in the middle of a string. If you need to do something to inner space, you would need to use another method such as replace():
s.replace(' ', '')
re.sub('\s+', ' ', s)

#It is often the case that you want to combine string stripping operations with some other kind of iterative processing, such as reading lines of data from a file (generator expression helps here):
with open('example.txt') as f:
    lines = (line.strip() for line in f)
    for line in lines:
        print(lines)

#The expression lines = (line.strip() for line in f) acts as a kind of data transform. It doesn't actually read the data into any kind of temporary list.
#It creates an iterator where all of the lines produced have the stripping operation applied to them.
#For more advanced stripping, you can also use the translate() method (more below)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
#2.12 - Sanitizing and Cleaning Up Text
        
#Problem: Someone has entered the text "pỹtĥön" into a form on your web page and you'd like to clean it up.
#Solution: The problem of sanitizing and cleaning up text applies to a wide variety of problems involving text parsing/data handling.
#At the most basic level, use basic string functions such as: str.upper() and str.lower() to convert text to standard cases.
#There are also simple replacements str.replace() and re.sub() which focus on removing or altering very specific character sequences. You can normalize with unicodedata.normalize() (See Section 2.9)
#If you want to take the sanitation process further, you can eliminate whole ranges of characters or strip diacritical markers with the str.translate() method:

s = 'pỹtĥön\fis\tawesome\r\n'
#If you print this statement it will return: pỹtĥönits     awesome
#If you enter s in the console it will return: 'pỹtĥön\x0cits\tawesome\r\n'

#First, cleanup whitespace by making a small translation table and use translate():
remap = {
    ord('\t') : ' ',
    ord('\f') : ' ',
    ord('\r') : None
}
a = s.translate(remap)
#Now when you enter a it will return: 'pỹtĥön is awesome\n'
#We can take this remap a step further by building much larger tables, removing all combining characters:
import sys
cmb_chrs = dict.fromkeys(c for c in range(sys.maxunicode)
                if unicodedata.combining(chr(c)))

b = unicodedata.normalize('NFD', a)
print(b.translate(cmb_chrs))

#A dictionary mapping every Unicode combining character to None is created using the dict.fromkeys()
#The original input is then normalized into a decomposed form using unicodedata.normalize()
#From there, the translate function is used to delete all of the accents. Similar techniques can be used to remove other kinds of characters (control chars, etc.)

#Here is a translation table that maps all Unicode decimal digit characters to their equivalent in ASCII:
digitmap = { c: ord('0') + unicodedata.digit(chr(c))
            for c in range(sys.maxunicode)
            if unicodedata.category(chr(c)) == 'Nd' }

#Entering the length of the digit map in the console returns 610
#Arabic digits
x = '\u0661\u0662\u0663'
print(x.translate(digitmap))

#Alternatively you can use the I/O decoding and encoding functions to clean up text. The idea is to do preliminary cleanup and then run it through combination of encode() and decode() to strip/alter it:
b = unicodedata.normalize('NFD', a)
b.encode('ascii', 'ignore').decode('ascii')
#The norm process decomposed the original text into characters along with separate combining characters.
#Then the ASCII simply discarded all of those characters at once, this only works if getting an ASCII representation is the final goal.

#Runtime performance can be a large issue with sanitizing text. In general, it should be as simple as possible for maximum efficiency.
#For replacements, str.replace() is often the fastest approach, even if you call it multiple times. To cleanup whitespace you could use:
def clean_spaces(s):
    s = s.replace('\r', '')
    s = s.replace('\t', ' ')
    s = s.replace('\f', ' ')
    return s

#On the other hand, translate is fast if you need to perform nontrivial char-to-char remapping or deletion. There is no one specific best method that works for all cases, so try different approaches and measure.
#Techniques similar to these can also be applied to bytes, including simple replacements, translation, and regular expressions.

