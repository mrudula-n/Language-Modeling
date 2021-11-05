"""
Language Modeling Project
Name:
Roll No:
"""

import language_tests as test

project = "Language" # don't edit this

### WEEK 1 ###

'''
loadBook(filename)
#1 [Check6-1]
Parameters: str
Returns: 2D list of strs
'''
def loadBook(filename):
    file=open(filename,"r")
    lines=file.readlines()
    file.close()
    sentance=[]
    for line in lines:
        nlines=line.split()
        sentance.append(nlines)
        lst1=[lst1 for lst1 in sentance if lst1!=[]]
    return lst1



'''
getCorpusLength(corpus)
#2 [Check6-1]
Parameters: 2D list of strs
Returns: int
'''
def getCorpusLength(corpus):
    count=0
    for list in corpus:
        count=count+len(list)
    return count


'''
buildVocabulary(corpus)
#3 [Check6-1]
Parameters: 2D list of strs
Returns: list of strs
'''
def buildVocabulary(corpus):
    empty_list=[]
    for list in corpus:
        for i in list:
            if i not in empty_list:
                empty_list.append(i)
    return empty_list


'''
countUnigrams(corpus)
#4 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to ints
'''
def countUnigrams(corpus):
    dictionary={}
    for i in corpus:
        for j in i:
            if j in dictionary:
                dictionary[j]+=1
            else:
                dictionary[j]=1
    return dictionary

'''
getStartWords(corpus)
#5 [Check6-1]
Parameters: 2D list of strs
Returns: list of strs
'''
def getStartWords(corpus):
    start_words=[]
    for i in corpus:
        word=i[0]
        if word not in start_words:
            start_words.append(word)
    return start_words

'''
countStartWords(corpus)
#5 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to ints
'''
def countStartWords(corpus):
    list=[]
    for i in corpus:
        word=i[0]
        list.append(word)
    words_dict=dict((i,list.count(i)) for i in list)
    return words_dict

'''
countBigrams(corpus)
#6 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to (dicts mapping strs to ints)
'''
def countBigrams(corpus):
    new_dict={}
    for i in corpus:
        for j in range(len(i)-1):
            if i[j] not in new_dict:
                new_dict[i[j]]={}
            if i[j+1] in new_dict[i[j]]:
                new_dict[i[j]][i[j+1]]+=1
            else:
                new_dict[i[j]][i[j+1]]=1
    return new_dict


### WEEK 2 ###

'''
buildUniformProbs(unigrams)
#1 [Check6-2]
Parameters: list of strs
Returns: list of floats
'''
def buildUniformProbs(unigrams):
    length=len(unigrams)
    list_element=1/length
    list=[]
    for i in range(length):
        list.append(list_element)
    return list

'''
buildUnigramProbs(unigrams, unigramCounts, totalCount)
#2 [Check6-2]
Parameters: list of strs ; dict mapping strs to ints ; int
Returns: list of floats
'''
def buildUnigramProbs(unigrams, unigramCounts, totalCount):
    values=unigramCounts.values()
    list=[i/totalCount for i in values]
    return list

'''
buildBigramProbs(unigramCounts, bigramCounts)
#3 [Check6-2]
Parameters: dict mapping strs to ints ; dict mapping strs to (dicts mapping strs to ints)
Returns: dict mapping strs to (dicts mapping strs to (lists of values))
'''
def buildBigramProbs(unigramCounts, bigramCounts):
    main_dictionary={}
    for prevWord in bigramCounts:
        word=[]
        prob=[]
        for key,value in bigramCounts[prevWord].items():
            word.append(key)
            prob.append(value/unigramCounts[prevWord])
            dictionary={}
            dictionary["words"]=word
            dictionary["probs"]=prob
        main_dictionary[prevWord]=dictionary
    return main_dictionary


'''
getTopWords(count, words, probs, ignoreList)
#4 [Check6-2]
Parameters: int ; list of strs ; list of floats ; list of strs
Returns: dict mapping strs to floats
'''
def getTopWords(count, words, probs, ignoreList):
    dict1={}
    result={words[i]:probs[i] for i in range(len(words)) if words[i] not in ignoreList}
    result1=sorted((value,key) for (key,value) in result.items())
    list=result1[-count:]
    dict1=dict([(k,v) for (v,k) in list])
    return dict1


'''
generateTextFromUnigrams(count, words, probs)
#5 [Check6-2]
Parameters: int ; list of strs ; list of floats
Returns: str
'''
from random import choices
def generateTextFromUnigrams(count, words, probs):
    string1=""
    for i in range(count):
        string2=choices(words, weights=probs)
        string1+=string2[0]+" "
    return string1

'''
generateTextFromBigrams(count, startWords, startWordProbs, bigramProbs)
#6 [Check6-2]
Parameters: int ; list of strs ; list of floats ; dict mapping strs to (dicts mapping strs to (lists of values))
Returns: str
'''
def generateTextFromBigrams(count, startWords, startWordProbs, bigramProbs):
    lines=""
    for i in range(count):
        list=lines.split()
        if len(lines)==0 or list[len(list)-1]==".":
            list1=choices(startWords, weights=startWordProbs)
            lines+=list1[0]+" "
        else:
            list2=choices(bigramProbs[list[len(list)-1]]["words"], weights=bigramProbs[list[len(list)-1]]["probs"])
            lines+=list2[0]+" "
    return lines


    
    
### WEEK 3 ###
ignore = [ ",", ".", "?", "'", '"', "-", "!", ":", ";", "by", "around", "over",
           "a", "on", "be", "in", "the", "is", "on", "and", "to", "of", "it",
           "as", "an", "but", "at", "if", "so", "was", "were", "for", "this",
           "that", "onto", "from", "not", "into" ]

'''
graphTop50Words(corpus)
#3 [Hw6]
Parameters: 2D list of strs
Returns: None
'''
import matplotlib.pyplot as plt;
import numpy as np
def graphTop50Words(corpus):
    words=buildVocabulary(corpus)
    count=getCorpusLength(corpus)
    unigramCount=countUnigrams(corpus)
    unigramProbs=buildUnigramProbs(words, unigramCount, totalCount=count)
    topWords=getTopWords(50, words, unigramProbs, ignore)
    graph=barPlot(topWords, "Top 50 Words")
    return graph


'''
graphTopStartWords(corpus)
#4 [Hw6]
Parameters: 2D list of strs
Returns: None
'''
def graphTopStartWords(corpus):
    return


'''
graphTopNextWords(corpus, word)
#5 [Hw6]
Parameters: 2D list of strs ; str
Returns: None
'''
def graphTopNextWords(corpus, word):
    return


'''
setupChartData(corpus1, corpus2, topWordCount)
#6 [Hw6]
Parameters: 2D list of strs ; 2D list of strs ; int
Returns: dict mapping strs to (lists of values)
'''
def setupChartData(corpus1, corpus2, topWordCount):
    return


'''
graphTopWordsSideBySide(corpus1, name1, corpus2, name2, numWords, title)
#6 [Hw6]
Parameters: 2D list of strs ; str ; 2D list of strs ; str ; int ; str
Returns: None
'''
def graphTopWordsSideBySide(corpus1, name1, corpus2, name2, numWords, title):
    return


'''
graphTopWordsInScatterplot(corpus1, corpus2, numWords, title)
#6 [Hw6]
Parameters: 2D list of strs ; 2D list of strs ; int ; str
Returns: None
'''
def graphTopWordsInScatterplot(corpus1, corpus2, numWords, title):
    return


### WEEK 3 PROVIDED CODE ###

"""
Expects a dictionary of words as keys with probabilities as values, and a title
Plots the words on the x axis, probabilities as the y axis and puts a title on top.
"""
def barPlot(dict, title):
    import matplotlib.pyplot as plt

    names = []
    values = []
    for k in dict:
        names.append(k)
        values.append(dict[k])

    plt.bar(names, values)

    plt.xticks(rotation='vertical')
    plt.title(title)

    plt.show()

"""
Expects 3 lists - one of x values, and two of values such that the index of a name
corresponds to a value at the same index in both lists. Category1 and Category2
are the labels for the different colors in the graph. For example, you may use
it to graph two categories of probabilities side by side to look at the differences.
"""
def sideBySideBarPlots(xValues, values1, values2, category1, category2, title):
    import matplotlib.pyplot as plt

    w = 0.35  # the width of the bars

    plt.bar(xValues, values1, width=-w, align='edge', label=category1)
    plt.bar(xValues, values2, width= w, align='edge', label=category2)

    plt.xticks(rotation="vertical")
    plt.legend()
    plt.title(title)

    plt.show()

"""
Expects two lists of probabilities and a list of labels (words) all the same length
and plots the probabilities of x and y, labels each point, and puts a title on top.
Note that this limits the graph to go from 0x0 to 0.02 x 0.02.
"""
def scatterPlot(xs, ys, labels, title):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    plt.scatter(xs, ys)

    # make labels for the points
    for i in range(len(labels)):
        plt.annotate(labels[i], # this is the text
                    (xs[i], ys[i]), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0, 10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    plt.title(title)
    plt.xlim(0, 0.02)
    plt.ylim(0, 0.02)

    # a bit of advanced code to draw a y=x line
    ax.plot([0, 1], [0, 1], color='black', transform=ax.transAxes)

    plt.show()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    test.week1Tests()
    # test.testCountBigrams()
    print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    test.runWeek1()

    ## Uncomment these for Week 2 ##

    print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    # test.testGenerateTextFromBigrams()
    test.week2Tests()

    print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
    test.runWeek2()


    ## Uncomment these for Week 3 ##

    print("\n" + "#"*15 + " WEEK 3 OUTPUT " + "#" * 15 + "\n")
    test.runWeek3()
