# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 15:08:01 2019

@author: pjhal
"""

""" Chapter 1: Data Structures and Algorithms """

#1.1 - Unpacking a Sequence into Separate Variables

#Problem: You have an N-element tuple or sequence that you would like to unpack into a collection of N variables
#Solution: Any sequence (or iterable) can be unpacked into variables using a simple assignment operation. The only requirement is that the number of variables and structure match the sequence.

p = (9, 42)
x, y = p

data = ['BlackMesa', 50, 93913.23, (2023, 12, 20)]

#name, shares, price, date = data
name, shares, price, (year, month, day) = data

#Unpacking actually works with any object that happens to be iterable, not just tuples or lists (strings, files, iterators, generators)
#When unpacking, you may sometimes want to discard certain values. Python has no special syntax, but you can often just pick a throwaway variable name for it, just make sure variable name isn't being used for something else!

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#1.2 - Unpacking Elements from Iterables of Arbitrary Length

#Problem: You need to unpack N elements from an iterable, but the iterable may be longer than N elements, causing a "too many values to unpack" exception
#Solution: Python "star expressions" can be used to address this problem. 

#Say you want to drop first/last grades of a course:

def drop_first_last(grades):
    first, *middle, last = grades
    return avg(middle)

def avg(number):
    total=0
    for i in number:
        total += i
    return total/len(number)

grades = (2, 4, 6, 8, 10, 12, 14, 16, 18, 20)
print (drop_first_last(grades))

#Or you have user records with name, email, phone number(s)
    
record = ('Bob', 'bob@example.com', '800-867-5309', '800-588-2300')
name, email, *phone_numbers = record

#phone_numbers variable will always be a list, even if there are no numbers unpacked. Thus, code won't have to account for possibility that it might not be a list or perform additional type checking

#Starred variable can also be the first one in a list, say you have a sequence of values for your company's sales figures for last eight quarters. You want to see how most recent quarter compares to average of first seven:

*trailing_qtrs, current_qtr = [100, 85, 72, 13, 94, 57, 104, 32]

def avg_comparison(avg, current_qtr):
    if avg == current_qtr:
        return True
    else:
        return False
     
trailing_avg = sum(trailing_qtrs)/len(trailing_qtrs)
print (avg_comparison(trailing_avg, current_qtr))
