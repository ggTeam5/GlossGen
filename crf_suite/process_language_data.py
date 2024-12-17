import re
import sklearn_crfsuite
from sklearn_crfsuite import metrics

# Funktion zum Einlesen und Verarbeiten der Datei
def process_file(filepath):
    data = []

    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        current_sentence = {"morphs": [], "glosses": []}

        for line in lines:
            line = line.strip()

            if line.startswith('\\m'):
                current_sentence["morphs"] = line[3:].split()

            elif line.startswith('\\g'):
                current_sentence["glosses"] = line[3:].split()

            elif line == '' or line.startswith('\\t') or line.startswith('\\l'):
                if current_sentence["morphs"] and current_sentence["glosses"]:
                    data.append(current_sentence)
                    current_sentence = {"morphs": [], "glosses": []}

    return data

# Feature-Berechnung für CRF
def word2features(sent, i):
    morph = sent["morphs"][i]
    features = {
        'bias': 1.0,
        'morph.lower()': morph.lower(),
        'morph[-3:]': morph[-3:],
        'morph[-2:]': morph[-2:],
        'morph.isupper()': morph.isupper(),
        'morph.isdigit()': morph.isdigit(),
    }
    if i > 0:
        prev_morph = sent["morphs"][i - 1]
        features.update({
            '-1:morph.lower()': prev_morph.lower(),
            '-1:morph[-3:]': prev_morph[-3:],
            '-1:morph.isupper()': prev_morph.isupper(),
        })
    else:
        features['BOS'] = True  # Satzanfang

    if i < len(sent["morphs"]) - 1:
        next_morph = sent["morphs"][i + 1]
        features.update({
            '+1:morph.lower()': next_morph.lower(),
            '+1:morph[-3:]': next_morph[-3:],
            '+1:morph.isupper()': next_morph.isupper(),
        })
    else:
        features['EOS'] = True  # Satzende

    return features

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent["morphs"]))]

def sent2labels(sent):
    # Initialisiere Labels als Standard "O"
    return ["O" for _ in sent["morphs"]]

def sent2tokens(sent):
    return sent["morphs"]

# Hauptprogramm: Datei einlesen, Features berechnen und CRF trainieren
if __name__ == "__main__":
    filepath = "lez-test-track2-uncovered-copy"
    data = process_file(filepath)

    print("--------data--------")
    print(data)

    # Aufteilen der Daten in Features und Labels
    X = [sent2features(s) for s in data]
    y = [sent2labels(s) for s in data]

    print("--------X--------")
    print(X)
    print("--------y--------")
    print(y)
    print("--------end--------")


    # CRF-Modell trainieren
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1,
        c2=0.1,
        max_iterations=100,
        all_possible_transitions=True
    )

    # Dummy-Training, da wir keine Labels haben
    # In der Realität sollten hier echte Labels genutzt werden
    crf.fit(X, y)

    # Ausgabe der Ergebnisse
    for sent in data:
        tokens = sent2tokens(sent)
        predictions = crf.predict([sent2features(sent)])[0]

        # Formatierung der Ausgabe
        result = [(tokens[i], sent["glosses"][i], predictions[i]) for i in range(len(tokens))]
        print(result)
