from os.path import join, dirname
import pickle

import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import SVC

try:
    from nlp.intent.feature_transformer import FeatureTransformer
except ImportError:
    from src.nlp.intent.feature_transformer import FeatureTransformer

s_schedule = ['lịch thi đấu', 'thời gian', 'thời gian thi đấu']
s_result = ['kết quả']
s_define = ['seagame', 'seagames', 'seagames là gì', 'seagame là gì', 'seagames là gì?',
            'seagame là gì?',
            'định nghĩa seagames', 'định nghĩa seagame', 'định nghĩa về seagames',
            'định nghĩa về seagame']
s_mascot = ['linh vật', 'con vật', 'biểu tượng', 'đại diện']
s_host = ['đăng cai', 'tổ chức', 'chủ nhà', 'đơn vị tổ chức']
s_ranking = ['bảng xếp hạng', 'bảng tổng sắp', 'huy chương']


class SVMModel:
    def __init__(self):
        # self.clf = self._init_pipeline()
        try:
            file_name = 'svm_model_ver2.sav'
            self.loaded_model = pickle.load(open(join(dirname(__file__), "model", file_name), 'rb'))
            print("Load successuful")
        except Exception as ex:
            print("Load model error: ",ex)

    @staticmethod
    def _init_pipeline():
        pipe_line = Pipeline([
            ("transformer", FeatureTransformer()),
            ("vect", CountVectorizer()),
            ("tfidf", TfidfTransformer()),
            # ("clf-svm", SGDClassifier(loss='log', penalty='l2', alpha=1e-3, n_iter=5, random_state=None))
            ("clf-svm",
             SVC(kernel='linear', class_weight='balanced', C=1.0, random_state=0, probability=True))
        ])

        return pipe_line

    def predict(self, sentence, entity):
        df = pd.DataFrame([{'feature': sentence}])
        # print(self.loaded_model.predict([sentence]))
        print(type(df['feature']))
        print(df['feature'])
        intent = self.loaded_model.predict(df['feature'])[0].strip()

        # Từ khóa
        if any(item.strip().lower() in sentence.strip().lower() for item in s_schedule):
            intent = 'schedule'
        elif entity.get("is_name"):
            intent = 'athele'

        confident = self.loaded_model.predict_proba(df["feature"])

        if intent in ['schedule', 'result']:
            if max(confident[0]) < 0.69:
                intent = 'chuaro'
        elif intent == 'rank':
            if entity.get("is_sport"):
                intent = 'schedule'
        if any(item.strip().lower() == sentence.strip().lower() for item in s_define):
            intent = 'define'

        if any(item.strip().lower() in sentence.strip().lower() for item in s_mascot):
            intent = 'mascot'

        if any(item.strip().lower() in sentence.strip().lower() for item in s_result):
            intent = 'result'

        if any(item.strip().lower() in sentence.strip().lower() for item in s_ranking):
            intent = 'rank'

        if any(item.strip().lower() in sentence.strip().lower() for item in s_host):
            intent = 'host'

        if sentence.strip().lower() == 'quốc gia':
            intent = 'list_countries'
        if sentence.strip().lower() == 'kết quả tổng sắp':
            intent = 'rank'

        return intent
