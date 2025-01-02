import sklearn_crfsuite
import process_morpheme_line
from sklearn_crfsuite import metrics
import translation_line_crf_most_frequent_labels
import process_morpheme_line
import sys

# Feature-Berechnung für CRF
def word2features(sent, i):
    word = sent[i][0]

    features = {
        'bias': 1.0,
        'word.lower()': word.lower(), # the morpheme itself
        'word.isupper()': word.isupper(), # Is the morpheme in capital letters? Perhaps remove?
        'word.istitle()': word.istitle(), # Is the morpheme in title case?
        'word.isdigit()': word.isdigit(), # Is the morpheme only digits?
        'word.length': len(word), # the morpheme length
    }
    if i > 0:
        word1 = sent[i-1][0]
        features.update({
            '-1:word.lower()': word1.lower(), # the previous morpheme
            '-1:word.length': len(word1), # the length of the previous morpheme
        })
    else:
        features['BOS'] = True # beginning of the sentence

    if i < len(sent)-1:
        word1 = sent[i+1][0]
        features.update({
            '+1:word.lower()': word1.lower(), # the next morpheme
            '+1:word.length': len(word1), # the length of the next morpheme
        })
    else:
        features['EOS'] = True # end of the sentence

    return features

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]


def sent2labels(sent):
    return [label for (token , label) in sent]


def sent2tokens(sent):
    return sent["morphs"]


#
def extract_language_name(filepath: str):
    return filepath.split("-")[0]



# Hauptprogramm: Datei einlesen, Features berechnen und CRF trainieren
if __name__ == "__main__":
    # filepathTrain = "lez-train-track2-uncovered"
    # filepathTest = "lez-test-track2-uncovered"
    print(sys.argv)
    if (len(sys.argv)) != 3:
        print("first argument should be filePathTrain, second argument should be filePathTest")
    filepathTrain = sys.argv[1]
    filepathTest = sys.argv[2]
    train_sents = process_morpheme_line.process_morpheme_line(filepathTrain, True) #returns list of list of tuples
    test_sents = process_morpheme_line.process_morpheme_line(filepathTest, True) #returns list of list of tuples
    
    print("test_sents: ",test_sents)

    # Aufteilen der Daten in Features und Labels
    X_train = [sent2features(s) for s in train_sents]
    y_train = [sent2labels(s) for s in train_sents]

    X_test = [sent2features(s) for s in test_sents]
    y_test = [sent2labels(s) for s in test_sents]

    # CRF-Modell trainieren
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1,
        c2=0.1,
        max_iterations=100,
        all_possible_transitions=True
    )
    crf.fit(X_train, y_train)

    labels = list(crf.classes_)

    y_pred = crf.predict(X_test)

    test_sents2 = process_morpheme_line.process_morpheme_line(filepathTest, False)
    
    labelDict = translation_line_crf_most_frequent_labels.most_frequent_label(test_sents2)

    for i in range(len(y_pred)):
        for j in range(len(y_pred[i])):
            if "stem" in y_pred[i][j]:
                (morph,gloss) = test_sents2[i][j]
                if morph in labelDict:
                    y_pred[i][j] = labelDict[morph]
                else:
                    y_pred[i][j] = "UNK"
    
    glossSentList = []

    for i in range(len(y_pred)):
        resStr = ""
        j = 0
        while j < len(y_pred[i]):
            if y_pred[i][j] == "-":
                resStr = resStr + y_pred[i][j]
                if j+1<len(y_pred[i]):
                    resStr = resStr + y_pred[i][j+1]
                    j += 2
                else:
                    j += 1
            else:
                if j != 0:
                    resStr = resStr + " " + y_pred[i][j]
                else:
                    resStr = resStr + y_pred[i][j]
                j += 1
        glossSentList.append(resStr)

outputFilePath = extract_language_name(filepathTest) + "-prediction.txt"
with open(outputFilePath,"w",encoding='utf-8') as file:
    for i in range(len(glossSentList)):
        file.write('\\t'+'\n')
        file.write('\\m'+'\n')
        file.write('\\g ' + glossSentList[i]+'\n')
        file.write('\\l'+'\n')
        file.write('\n')