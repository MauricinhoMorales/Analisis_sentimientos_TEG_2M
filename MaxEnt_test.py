import collections
import nltk.classify.util, nltk.metrics
from nltk.tokenize import word_tokenize
from nltk.classify import NaiveBayesClassifier, MaxentClassifier, SklearnClassifier
import csv
import random
from nltk.corpus import stopwords
import itertools
from nltk.collocations import BigramCollocationFinder
# nltk.download()

posdata = []
with open('positive-negative-data//positive-data.csv', 'rt') as myfile:	
	reader = csv.reader(myfile, delimiter=',')
	for val in reader:
		posdata.append(val[0])		

negdata = []
with open('positive-negative-data//negative-data.csv', 'rt') as myfile:	
	reader = csv.reader(myfile, delimiter=',')
	for val in reader:
		negdata.append(val[0])

def word_split(data):
    data_new = []
    for word in data:
        word_filter = [i.lower() for i in word.split()]
        data_new.append(word_filter)
    return data_new

def word_split_sentiment(data):
	data_new = []
	for (word, sentiment) in data:
		word_filter = [i.lower() for i in word.split()]
		data_new.append((word_filter, sentiment))
	return data_new
	
def word_feats(words):
    return dict([(word, True) for word in words])

stopset = set(stopwords.words('english')) - set(('over', 'under', 'below', 'more', 'most', 'no', 'not', 'only', 'such', 'few', 'so', 'too', 'very', 'just', 'any', 'once'))
     
def stopword_filtered_word_feats(words):
    return dict([(word, True) for word in words if word not in stopset])

def bigram_word_feats(words, score_fn=nltk.collocations.BigramAssocMeasures.chi_sq, n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbestnbest(score_fn, n)
    """
    print words
    for ngram in itertools.chain(words, bigrams): 
		if ngram not in stopset: 
			print ngram
    exit()
    """    
    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])
    
def bigram_word_feats_stopwords(words, score_fn=nltk.collocations.BigramAssocMeasures.chi_sq, n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    """
    print words
    for ngram in itertools.chain(words, bigrams): 
		if ngram not in stopset: 
			print ngram
    exit()
    """    
    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams) if ngram not in stopset])

def evaluate_classifier(featx):
    
    negfeats = [(featx(f), 'neg') for f in word_split(negdata)]
    posfeats = [(featx(f), 'pos') for f in word_split(posdata)]
    
    negcutoff = len(negfeats)*3/4
    poscutoff = len(posfeats)*3/4
    
    trainfeats = negfeats[:int(negcutoff)] + posfeats[:int(poscutoff)]
    testfeats = negfeats[int(negcutoff):] + posfeats[int(poscutoff):]
    
    classifierName = 'Maximum Entropy'
    classifier = MaxentClassifier.train(trainfeats, 'GIS', trace=0, encoding=None, labels=None, gaussian_prior_sigma=0, max_iter = 1)
    
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)
    
    for i, (feats, label) in enumerate(testfeats):
        refsets[label].add(i)
        observed = classifier.classify(feats)
        testsets[observed].add(i)
    
    accuracy = nltk.classify.util.accuracy(classifier, testfeats)
    
    print ('')
    print ('---------------------------------------')
    print ('SINGLE FOLD RESULT ' + '(' + classifierName + ')')
    print ('---------------------------------------')
    print ('accuracy:', accuracy)
    

evaluate_classifier(word_feats)
evaluate_classifier(stopword_filtered_word_feats)
evaluate_classifier(bigram_word_feats)	
evaluate_classifier(bigram_word_feats_stopwords)