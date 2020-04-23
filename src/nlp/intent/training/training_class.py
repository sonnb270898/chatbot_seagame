import pandas as pd
from model import Model
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import accuracy_score
import pickle


class TextClassificationPredict(object):
    def __init__(self):
        self.x_train, self.x_test, self.y_train, self.y_test = self.get_train_data()
        self.cross_val_and_predict()

    def get_train_data(self):
        data = []
        file = open('data.txt', 'r', encoding='utf-8-sig')
        i = 0
        for line in file:
            content = line.strip().split(':')[0].strip()
            target = line.strip().split(':')[1].strip()
            data.append({"feature": content, "target": target})
            print(i)
            i = i + 1
        df = pd.DataFrame(data)
        x_train, x_test, y_train, y_test = train_test_split(df['feature'], df['target'],
                                                            test_size=0.3, random_state=42)
        return x_train, x_test, y_train, y_test

    def cross_val_and_predict(self):
        model = Model()
        clf = model.clf.fit(self.x_train, self.y_train)
        file_name = 'svm_model.sav'
        pickle.dump(clf, open(file_name, 'wb'))
        score = cross_val_score(clf, self.x_test, self.y_test, verbose=0)
        print(score)
# tcp = TextClassificationPredict()
