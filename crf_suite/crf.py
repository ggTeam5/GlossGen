import matplotlib.pyplot as plt
plt.style.use('ggplot')

from itertools import chain

import nltk
import sklearn
import scipy.stats
from sklearn.metrics import make_scorer
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RandomizedSearchCV

import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics

# own imports
import process_morpheme_line
import translation_line_crf_most_frequent_labels

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
        postag1 = sent[i-1][1]
        features.update({
            '-1:word.lower()': word1.lower(), # the previous morpheme
            '-1:word.length': len(word1), # the length of the previous morpheme
        })
    else:
        features['BOS'] = True # at the beginning of the sentence

    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.update({
            '+1:word.lower()': word1.lower(), # the next morpheme
            '+1:word.length': len(word1), # the length of the next morpheme
        })
    else:
        features['EOS'] = True # at the end of the sentence

    return features

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, postag, label in sent]

def sent2tokens(sent):
    return [token for token, postag, label in sent]

testFilepath = "lez-test-track2-uncovered"
trainingFilepath = "lez-dev-track2-uncovered"
test_sents = process_morpheme_line.process_morpheme_line(testFilepath, False)
train_sents = process_morpheme_line.process_morpheme_line(trainingFilepath, False)
dict_majority_label = translation_line_crf_most_frequent_labels.most_frequent_label(filePath=trainingFilepath)

X_train = [sent2features(s) for s in train_sents]
y_train = [sent2labels(s) for s in train_sents]

X_test = [sent2features(s) for s in test_sents]
y_test = [sent2labels(s) for s in test_sents] 

crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=True
)
crf.fit(X_train, y_train)