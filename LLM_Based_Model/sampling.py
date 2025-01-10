import heapq

def uniqueWords (sentence: str):
    words = sentence.split()
    for i in range(len(words)):
        word = sentence[i]
        if word[0].isupper() and len(word)>1 and word[1:].islower():
            words[i]=word.lower()

    return set(words)

def wordRecall (trainSentence: str, testSentence: str):
    uniqueTestWords = uniqueWords(testSentence)
    return len(uniqueWords(trainSentence) & uniqueTestWords) / len(uniqueTestWords)

# returns list of tuples. One tuples contains the transcription line, the morphological line, the glossing line and the translation line
def n_highest_wordRecall_sentences(n: int, trainFilePath: str, testSentence: str):
    sentList = []
    with open(trainFilePath, "r",encoding='utf-8') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            if lines[i].startswith("\\t "):
                line = lines[i].strip("\\t ")
                res = wordRecall(line, testSentence)
                sentList.append((res,lines[i],lines[i+1],lines[i+2],lines[i+3]))
        sentList = heapq.nlargest(n,sentList, key=lambda x: x[0])
        resList = []
        for _,tline,mline,gline,lline in sentList:
            resList.append(tline)
            resList.append(mline)
            resList.append(gline)
            resList.append(lline)
    return resList
