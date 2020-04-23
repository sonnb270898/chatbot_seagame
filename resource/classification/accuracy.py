import pandas as pd
from svm_model import SVMModel
import pickle


class TextClassificationPredict(object):
    def __init__(self):
        self.test = None

    def accuracy(self):
        #  train data
        data = []
        file = open('E:\\20183\\Thực tập kĩ thuật\\chatbot-seagame\\data_44k.txt','r',encoding = 'utf-8-sig')
        i = 0
        for line in file:
            content = line.strip().split(':')[0].strip()
            target = line.strip().split(':')[1].strip()
            data.append({"feature": content, "target": target})
            print(i)
            i = i+1
        df_data = pd.DataFrame(data)
        train_dataset = df_data.sample(frac = 0.7,random_state = 0)
        test_dataset  = df_data.drop(train_dataset.index)

        model = SVMModel()
        clf = model.clf.fit(train_dataset["feature"], train_dataset.target)
        predicted = clf.predict(test_dataset["feature"])
        a = test_dataset['target'].values
        count = 0
        lenght = len(a)
        for i in range(len(predicted)):
            if predicted[i]==a[i]:
                count=count+1
        accuracy = count/lenght
        print(accuracy)

tcp = TextClassificationPredict()
tcp.accuracy()