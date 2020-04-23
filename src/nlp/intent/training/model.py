from sklearn.naive_bayes import ComplementNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from pyvi import ViTokenizer


class Model(object):
    def __init__(self):
        self.clf1 = RandomForestClassifier(n_estimators=50, random_state=1)
        self.clf2 = SVC(C=0.1, random_state=1)  # ,class_weight='balanced',probability=True
        self.clf3 = ComplementNB()
        self.clf = self.init_model()

    def tokenize(self, text):
        token = [word for word in ViTokenizer.tokenize(text).split(' ')]
        return token

    def init_model(self):
        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(tokenizer=self.tokenize)),
            ('vm', VotingClassifier(
                estimators=[('clf1', self.clf1), ('clf2', self.clf2), ('clf3', self.clf3)],
                voting='hard'))
        ])
        params = dict(vm__clf1__n_estimators=[50, 100, 200], vm__clf2__C=[0.1, 10, 100])
        gs = GridSearchCV(pipeline, param_grid=params, cv=3)
        return gs
        # return pipeline
