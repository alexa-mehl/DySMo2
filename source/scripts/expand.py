'''
Created on 06.09.2012
Provides a function to expand single options to a list if necessary.
@author: Tommy Beckmann
'''


def expandToList(value, items):
    retVal = []
    for dummy in items:
        retVal.append(value)
    return retVal
