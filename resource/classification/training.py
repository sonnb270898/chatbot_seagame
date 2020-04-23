import pandas as pd
from svm_model import SVMModel
import pickle


class TextClassificationPredict(object):
    def __init__(self):
        self.test = None

    def get_train_data(self):
        #  train data
        train_data = []
        file = open('E:\\20183\\Thực tập kĩ thuật\\chatbot-seagame\\data_17k_ver2.txt','r',encoding = 'utf-8-sig')
        i = 0
        for line in file:
            content = line.strip().split(':')[0].strip()
            target = line.strip().split(':')[1].strip()
            train_data.append({"feature": content, "target": target})
            print(i)
            i = i+1
        df_train = pd.DataFrame(train_data)

        model = SVMModel()
        clf = model.clf.fit(df_train["feature"], df_train.target)
        file_name = 'svm_model_ver2.sav'
        pickle.dump(clf, open(file_name, 'wb'))

tcp = TextClassificationPredict()
tcp.get_train_data()