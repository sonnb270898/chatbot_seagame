import pandas as pd
from svm_model import SVMModel
from os.path import join, dirname
import pickle
# a = join(dirname(__file__),'hehe/svm_model.sav')
# print(a)
class TextClassificationPredict(object):
    def __init__(self):
        self.test = None

    def predict(self,question):
        #  test data
        test_data = []
        test_data.append({"feature": question, "target": "seagames_là_gì"})
        df_test = pd.DataFrame(test_data)

        # init model naive bayes
        model = SVMModel()
        file_name = 'svm_model.sav'
        # loaded_model = pickle.load(open('/'.join(os.getcwd().split('\\')) + '/'+file_name, 'rb'))
        loaded_model = pickle.load(open(join(dirname(__file__),'svm_model.sav'), 'rb'))

        predicted = loaded_model.predict(df_test["feature"])

        # Print predicted result
        # print (predicted)
        # print (loaded_model.predict_proba(df_test["feature"]))
        return predicted

# cls = TextClassificationPredict()
# cls.predict('lịch thi đấu ngày mai')