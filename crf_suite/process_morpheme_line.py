import string

#TODO: question: how about stems with only upper case letters (e.g. FIFA, WHO, TUM, etc.)

def processGloss(gloss):
    if gloss.isupper() or (gloss in string.punctuation):
        return gloss
    elif not gloss.isupper() and not any(char in string.punctuation for char in gloss): return "stem"
    else:
        splittedGloss = gloss.split('.')
        for i in range(0,len(splittedGloss)):
            splittedGloss[i] = processGloss(splittedGloss[i])
        return '.'.join(splittedGloss)



if __name__ == "__main__":
    filepath = "lez-test-track2-uncovered-copy"

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
                        wordList.append((morpheme[k],processGloss(gloss[k])))
                        if k < len(gloss)-1:
                            wordList.append(("-","-"))
                lineList.append(wordList)
    print(lineList)