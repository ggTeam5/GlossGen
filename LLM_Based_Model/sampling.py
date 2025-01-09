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

def n_highest_wordRecall_sentences(n: int, trainFilePath: str): 
    # TODO
    return []
