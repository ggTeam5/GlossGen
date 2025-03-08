import string

#TODO: question: how about stems with only upper case letters (e.g. FIFA, WHO, TUM, etc.)
#TODO: 
# what if ",." --> should be "stem,.stem" ?
def processGloss(gloss):
    punctuations = string.punctuation + "«?»..."
    containsLetter = False
    for char in gloss:
        if not char in punctuations:
            containsLetter = True
    if not containsLetter:
        return gloss
    splittedGloss = gloss.split('.')
    for i in range(0,len(splittedGloss)):
        splittedGloss[i] = (splittedGloss[i] if gloss.isupper() else "stem")
    return '.'.join(splittedGloss)


# returns list with mapping for each morpheme to its label in the glossing line
def process_morpheme_line(filepath, replaceStems):
    lineList = []                                    #list(list(tupel(word,gloss)))

    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        for i in range(0,len(lines)):
            wordList = []                            #list(tupel(word,gloss))
            if lines[i].startswith('\\m'):
                morphemeLine = lines[i].split('\\m')[1].strip()
                glossLine = lines[i+1].split('\\g')[1].strip()
                morphemeLineList = morphemeLine.split()
                glossLineList = glossLine.split()
                for j in range(0,len(glossLineList)):
                    morpheme = morphemeLineList[j].split('-')
                    gloss = glossLineList[j].split('-')
                    for k in range(0,len(gloss)):
                        if replaceStems:
                            wordList.append((morpheme[k],processGloss(gloss[k])))
                        else:
                            wordList.append((morpheme[k],gloss[k]))
                        if k < len(gloss)-1:
                            wordList.append(("-","-"))
                lineList.append(wordList)

    return lineList