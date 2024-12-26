import sklearn_crfsuite
import process_morpheme_line
from sklearn_crfsuite import metrics


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


# Hauptprogramm: Datei einlesen, Features berechnen und CRF trainieren
if __name__ == "__main__":
    filepath = "lez-test-track2-uncovered"
    data = process_morpheme_line.process_morpheme_line(filepath, False) #returns list of tuples

    splitIndex = (int) (0.8*len(data))
    train_sents = data[0:splitIndex]
    test_sents = data[splitIndex:]

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

    print('y_pred: ',y_pred)

    res = metrics.flat_f1_score(y_test, y_pred,
                      average='weighted', labels=labels)
    
    print(res)







    # # Ausgabe der Ergebnisse
    # for sent in data:
    #     tokens = sent2tokens(sent)
    #     predictions = crf.predict([sent2features(sent)])[0]
    #     # Formatierung der Ausgabe
    #     result = [(tokens[i], sent["glosses"][i], predictions[i]) for i in range(len(tokens))]
    #     print(result)
