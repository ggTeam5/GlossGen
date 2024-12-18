import process_morpheme_line

def most_frequent_label(filePath):

    morphemeDict = {}

    morphemList = process_morpheme_line.process_morpheme_line(filePath,False)

    for i in range (0,len(morphemList)):
        for (morph,label) in morphemList[i]:
            if process_morpheme_line.processGloss(morph) == "stem":    
                if morph in morphemeDict:
                    internalDict = morphemeDict[morph]
                    if label in internalDict:
                        internalDict[label] = internalDict[label] + 1
                    else:
                        internalDict[label] = 1
                else:
                    internalDict = {
                        label: 1
                    }
                    morphemeDict[morph] = internalDict
    
    resultDict = {}

    for morph in morphemeDict:
        internalDict = morphemeDict[morph]
        bestLabelNumber = 0
        bestlabel = None
        for label in internalDict:
            if internalDict[label] > bestLabelNumber: #TODO: what if two labels have same frequency?
                bestLabelNumber = internalDict[label]
                bestlabel = label
        resultDict[morph] = bestlabel
    
    return resultDict