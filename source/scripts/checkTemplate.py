'''
Created on 05.09.2012

@author: Tommy
'''
# Idea for this file: If you generate your template files automatically,
#                     you don t need these checks!

import sys


## Check whether the global Save list form every mode have the same number of
#  entries
#  @return: Array with the output variabels to save
def globalSaveList(mParam, model):
    # help list contains all names to save for every single mode
    result = []
    for count, dummy in enumerate(mParam.MODELNAMELIST):
    #is there a difference between the globalSaveList and the arr save list?
        if not mParam.outputVariablesToSave[count + 1]:
            result.append(model.getGlSaveList())
        else:
            if(len(mParam.outputVariablesToSave[count + 1]) is not
               len(model.getGlSaveList())):
                # error save list must have the same length
                sys.exit("""Error: globalSaveList and individual modeSaveList
                             must have the same length!""")
            else:
                #everything OK
                result.append(mParam.outputVariablesToSave[count + 1])

    return result


def allEntSameLenght(mParam):
    modeNum = len(mParam.MODELNAMELIST)
    if (len(mParam.TOOLS) is not modeNum or len(mParam.SOLVERS) is not modeNum):
        sys.exit("""The Entries MODELNAMELIST, TOOLS and SOLVERS in your
        template must have the same length!""")
