#TODO: question: how about stems with only upper case letters (e.g. FIFA, WHO, TUM, etc.)

def processGloss(gloss):
    wordList = gloss.split('-')
    for i in range(0,len(wordList)):
        if not wordList[i].isupper():
            wordList[i] = "stem"

    return '-'.join(wordList)


if __name__ == "__main__":
    filepath = "lez-test-track2-uncovered-copy" #TODO: needs to be replaced

    lineList = [] #list(list(tupel(word,gloss)))

    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        for i in range(0,len(lines)):
            wordList = [] #list(tupel(word,gloss))
            if lines[i].startswith('\\m'):
                morphemeLine = lines[i].split('\\m')[1].strip()
                glossLine = lines[i+1].split('\\g')[1].strip()
                morphemeLineList = morphemeLine.split()
                glossLineList = glossLine.split()
                for j in range(0,len(glossLineList)):
                    morpheme = morphemeLineList[j]
                    gloss = glossLineList[j]
                    wordList.append((morpheme, processGloss(gloss)))
                lineList.append(wordList)
    print(lineList)