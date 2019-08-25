# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 16:30:35 2019

@author: pjhal
"""

""" Chapter 2: Strings and Text (Parts 5-8) """

#2.5 - Searching and Replacing Text

#Problem: You want to search for and replace a text pattern in a string.
#Solution: For simple literal patterns, use the str.replace() method:
text = "yes, but no, but yes, but no, but yes"
text.replace('yes', 'yeah')

#For a more complicated pattern, the sub() function/method in the [re] module will be more comprehensive:
text = 'Today is 8/25/2019. TwitchCon starts 9/27/2019.'
import re
re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text)

#The first argument to sub() is the pattern to match and the second argument is the replacement pattern.
#Backslashed digits such as \3 refer to capture group numbers in the pattern. For repeated subs of the same pattern, try compiling first:
datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
datepat.sub(r'\3-\1-\2', text)

#For more complicated substitutions, it's possible to specify a sub callback function instead:
from calendar import month_abbr
def change_date(m):
    mon_name = month_abbr[int(m.group(1))]
    return '{} {} {}'.format(m.group(2), mon_name, m.group(3))

#As input, the argument to the sub callback is a match object, as returned by match() or find(). Use the .group() method to extract specific parts of the match.
#If you want to know how many subs were made in addition to getting the replacement text, use re.subn() instead:
newtext, n = datepat.subn(r'\3-\1-\2', text)
print(newtext)
print(n)

#There isn't much to regular expression search/replace other than the sub() method shown. The trickiest part is specifying the regular expression pattern.

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#2.6 - Searching and Replacing Case-Insensitive Text

#Problem: You need to search for and possibly replace text in a case-insensitive manner
#Solution: To perform case-insensitive text operations, you need to use the [re] module and supply the re.IGNORECASE flag to various operations:
text = 'UPPER PYTHON, lower python, Mixed Python'
re.findall('python', text, flags=re.IGNORECASE)
#This will print ['PYTHON', 'python', 'Python'] in the console

re.sub('python', 'snake', text, flags=re.IGNORECASE)
#This time it will print 'UPPER snake, lower snake, Mixed snake', which reveals a limitation that replacing text won't match the case of matched text.
#You can use a support function to fix this:
def matchcase(word):
    def replace(m):
        text = m.group()
        if text.isupper():
            return word.upper()
        elif text.islower():
            return word.lower()
        elif text[0].isupper():
            return word.capitalize()
        else:
            return word
    return replace

#This can then be used as such:
re.sub('python', matchcase('snake'), text, flags=re.IGNORECASE)
#Now it will print 'UPPER SNAKE, lower snake, Mixed Snake' as desired

#For simple cases, simply providing the re.IGNORECASE is sufficient for performing case-insensitive matching. However, this may not be enough for certain kinds of Unicode matching involving case folding (See Section 2.10)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#2.7 - Specifying a Regular Expression for the Shortest Match

#Problem: You're trying to match a text pattern using regular expressions, but it is identifying the longest possible matches of a pattern. Instead, you would like to change it to find the shortest possible match.
#Solution: This problem frequently arises in patterns that attempt to match text inside a pair of start/end delimiters (quoted string):
str_pat = re.compile(r'\"(.*)\"')
text1 = 'Computer says "no."'
print(str_pat.findall(text1))

text2 = 'Computer says "no." Phone says "yes."'
print(str_pat.findall(text2))

#The pattern r'\"(.*)\"' is attempting to match text enclosed inside quotes. The * operator matches based on finding the longest match possible (thus why it incorrectly matches the two quoted strings).
#You can fix this by adding the ? modifier after the * operator:
str_pat = re.compile(r'\"(.*?)\"')
print(str_pat.findall(text2))

#This now gives us ['no.', 'yes'.]

#This addresses a common problem encountered when writing regular expressions involving the dot (.) character. The dot matches any character except a newline in a pattern.
#If you bracket the dot with starting/ending text (like a quote), matching will try to find the longest possible match to the pattern. This causes multiple occurrences of the starting/ending text to be skipped altogether.
#Adding the ? after operators such as * or + forces the matching algorithm to look for the shortest possible match instead.

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#2.8 - Writing a Regular Expression for Multiline Patterns

#Problem: You're trying to match a block of text using a regular expression, but you need the match to span multiple lines.
#Solution: This problem can often arise in patterns that use the dot (.) to match any character but forget to account for the fact that it doesn't match newlines. Say you were matching C-style comments:
comment = re.compile(r'/\*(.*?)\*/')
text1 = '/* this is a comment */'
text2 = '''/* this is a
              multiline comment */
'''

print(comment.findall(text1))
print(comment.findall(text2))

#Notice there is nothing printed for text2, we can fix this by adding support for newlines:
comment = re.compile(r'/\*((?:.|\n)*?)\*/')
print(comment.findall(text2))

#(?:.|\n) specifies a noncapture group (it defines a group for the purposes of matching, but the group is not captured separately or numbered)

#The re.compile() function accepts a flag, re.DOTALL, which makes the . in a regular expression match all characters, including newlines:
comment = re.compile(r'/\*(.*?)\*/', re.DOTALL)
print(comment.findall(text2))

#Using the re.DOTALL flag works fine for simple cases, but can be problematic if you're working with extremely complicated patterns or a mix of separate regular expressions that have been combined.
#Expressions can be combined for the purpose of tokenizing (Section 2.18) but if given the choice, it is usually better to define your regular expression pattern so that it works without the need for extra flags.