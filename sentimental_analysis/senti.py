import nltk
import random
#from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize
# import sys  
# reload(sys)  
# sys.setdefaultencoding('utf8')


class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf
    
short_pos = open("/media/pc-51/31542391-e61d-4a5a-b525-42933cdeae98/reshma_backup/python/fulldocs/twitter/sourcecode/twitter/short_reviews/positive.txt","r").read()
short_neg = open("/media/pc-51/31542391-e61d-4a5a-b525-42933cdeae98/reshma_backup/python/fulldocs/twitter/sourcecode/twitter/short_reviews/negative.txt","r").read()

# move this up here
all_words = []
documents = []


#  j is adject, r is adverb, and v is verb
#allowed_word_types = ["J","R","V"]
allowed_word_types = ["J"]

for p in short_pos.split('\n'):
    documents.append( (p, "pos") )
    words = word_tokenize(p)
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())

    
for p in short_neg.split('\n'):
    documents.append( (p, "neg") )
    words = word_tokenize(p)
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())


# save_documents = open("/media/pc15/DATA/python/twiter/twitter/pickled_algos/documents.pickle","rb")
# pickle.dump(documents, save_documents)
# save_documents.close()
open_file = open("/media/pc-51/31542391-e61d-4a5a-b525-42933cdeae98/reshma_backup/python/fulldocs/twitter/sourcecode/twitter/pickled_algos/documents.pickle", "rb")
documents = pickle.load(open_file)
open_file.close()

all_words = nltk.FreqDist(all_words)


word_features = list(all_words.keys())[:5000]

open_file = open("/media/pc-51/31542391-e61d-4a5a-b525-42933cdeae98/reshma_backup/python/fulldocs/twitter/sourcecode/twitter/pickled_algos/word_features5k.pickle", "rb")
word_features = pickle.load(open_file)
open_file.close()


# save_word_features = open("/media/pc15/DATA/python/twiter/twitter/pickled_algos/word_features5k.pickle","rb")
# pickle.dump(word_features, save_word_features)
# save_word_features.close()


def find_features(document):
    words = word_tokenize(document)
    features = {}
    # print("words",words)
    for w in word_features:
        features[w] = (w in words)

    return features

featuresets = [(find_features(rev), category) for (rev, category) in documents]

random.shuffle(featuresets)
print(len(featuresets))

training_set = featuresets[:1000]
testing_set = featuresets[10000:]




# classifier = nltk.NaiveBayesClassifier.train(training_set)
# print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set))*100)
# classifier.show_most_informative_features(15)

###############
# save_classifier = open("/media/pc15/DATA/python/twiter/twitter/pickled_algos/originalnaivebayes5k.pickle","rb")
# pickle.dump(classifier, save_classifier)
# save_classifier.close()
open_file = open("/media/pc-51/31542391-e61d-4a5a-b525-42933cdeae98/reshma_backup/python/fulldocs/twitter/sourcecode/twitter/pickled_algos/originalnaivebayes5k.pickle", "rb")
classifier = pickle.load(open_file)
open_file.close()

open_file = open("/media/pc-51/31542391-e61d-4a5a-b525-42933cdeae98/reshma_backup/python/fulldocs/twitter/sourcecode/twitter/pickled_algos/BernoulliNB_classifier5k.pickle", "rb")
BernoulliNB_classifier = pickle.load(open_file)
open_file.close()

open_file = open("/media/pc-51/31542391-e61d-4a5a-b525-42933cdeae98/reshma_backup/python/fulldocs/twitter/sourcecode/twitter/pickled_algos/MNB_classifier5k.pickle", "rb")
MNB_classifier = pickle.load(open_file)
open_file.close()

open_file = open("/media/pc-51/31542391-e61d-4a5a-b525-42933cdeae98/reshma_backup/python/fulldocs/twitter/sourcecode/twitter/pickled_algos/LogisticRegression_classifier5k.pickle", "rb")
LogisticRegression_classifier = pickle.load(open_file)
open_file.close()

open_file = open("/media/pc-51/31542391-e61d-4a5a-b525-42933cdeae98/reshma_backup/python/fulldocs/twitter/sourcecode/twitter/pickled_algos/LinearSVC_classifier5k.pickle", "rb")
LinearSVC_classifier = pickle.load(open_file)
open_file.close()

open_file = open("/media/pc-51/31542391-e61d-4a5a-b525-42933cdeae98/reshma_backup/python/fulldocs/twitter/sourcecode/twitter/pickled_algos/SGDC_classifier5k.pickle", "rb")
SGDC_classifier = pickle.load(open_file)
open_file.close()

# MNB_classifier = SklearnClassifier(MultinomialNB())
# MNB_classifier.train(training_set)
# print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)

# save_classifier = open("/media/pc15/DATA/python/twiter/twitter/pickled_algos/MNB_classifier5k.pickle","rb")
# pickle.dump(MNB_classifier, save_classifier)
# save_classifier.close()

# BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
# BernoulliNB_classifier.train(training_set)
# print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)

# save_classifier = open("/media/pc15/DATA/python/twiter/twitter/pickled_algos/BernoulliNB_classifier5k.pickle","rb")
# pickle.dump(BernoulliNB_classifier, save_classifier)
# save_classifier.close()

# LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
# LogisticRegression_classifier.train(training_set)
# print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

# save_classifier = open("/media/pc15/DATA/python/twiter/twitter/pickled_algos/LogisticRegression_classifier5k.pickle","rb")
# pickle.dump(LogisticRegression_classifier, save_classifier)
# save_classifier.close()


# LinearSVC_classifier = SklearnClassifier(LinearSVC())
# LinearSVC_classifier.train(training_set)
# print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)

# save_classifier = open("/media/pc15/DATA/python/twiter/twitter/pickled_algos/LinearSVC_classifier5k.pickle","rb")
# pickle.dump(LinearSVC_classifier, save_classifier)
# # save_classifier.close()


# #NuSVC_classifier = SklearnClassifier(NuSVC())
# #NuSVC_classifier.train(training_set)
# #print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)


# SGDC_classifier = SklearnClassifier(SGDClassifier())
# SGDC_classifier.train(training_set)
# print("SGDClassifier accuracy percent:",nltk.classify.accuracy(SGDC_classifier, testing_set)*100)

# save_classifier = open("/media/pc15/DATA/python/twiter/twitter/pickled_algos/SGDC_classifier5k.pickle","rb")
# pickle.dump(SGDC_classifier, save_classifier)
# save_classifier.close()


voted_classifier = VoteClassifier(
        classifier,
        LinearSVC_classifier,
        MNB_classifier,
        BernoulliNB_classifier,
        LogisticRegression_classifier,
        SGDC_classifier
    )


# voted_classifier = VoteClassifier(classifier)                                  

def sentiment(text):
    feats = find_features(text)
    # feats1 = len(feats)
    # numneg = len(voted_classifier.classify(feats))
    # numpos = len(voted_classifier.confidence(feats))
    # print("lengths python",feats1,numneg) 
    return voted_classifier.classify(feats),voted_classifier.confidence(feats)
