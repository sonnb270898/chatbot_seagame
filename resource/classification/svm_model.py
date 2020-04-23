import os, sys
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC
from feature_transformer import FeatureTransformer
from sklearn.preprocessing import StandardScaler

class SVMModel(object):
    def __init__(self):
        self.clf = self._init_pipeline()

    @staticmethod
    def _init_pipeline():
        pipe_line = Pipeline([
            ("transformer", FeatureTransformer()),
            ("vect", CountVectorizer()),
            ("tfidf", TfidfTransformer()),
            # ("clf-svm", SGDClassifier(loss='log', penalty='l2', alpha=1e-3, n_iter=5, random_state=None))
            ("clf-svm", SVC(kernel='linear', class_weight='balanced', C=1.0, random_state=0,probability=True))
        ])

        return pipe_line