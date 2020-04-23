from os.path import join, dirname
from collections import defaultdict

try:
    from utils.file_io import read
except ImportError:
    from src.utils.file_io import read

SPORT = read(filename=join(dirname(__file__), '../../data/sport.txt'), format_ex="txt")
SPORT = [item.strip().lower() for item in SPORT.split("\n")]

COUNTRY = read(filename=join(dirname(__file__), '../../data/country.json'), format_ex="json")
COUNTRY = [item["ten"].lower().strip() for item in COUNTRY]

NAME = read(filename=join(dirname(__file__), '../../data/persion_name.json'), format_ex="json")


class NERPredict:
    def __init__(self):
        self.entities = defaultdict(list)

    def max_match(self, sentence):
        i = len(sentence)
        if i < 1:
            return ''
        while i >= 1:
            first_word = sentence[:i]
            w = ' '.join(first_word).lower()
            if w in COUNTRY:
                self.entities['is_country'].append(w)
                break
            if w in NAME:
                self.entities['is_name'].extend(NAME[w])
                break
            if w in SPORT:
                self.entities['is_sport'].append(w)
                break
            i -= 1
        if i == 0:
            self.max_match(sentence[i + 1:])
        else:
            self.max_match(sentence[i:])

    def predict(self, sentence):
        """

        :param sentence:
        :return:
        """
        self.max_match(sentence.split(' '))
        return self.entities

# ner = NER('Nỗi lo duy nhất với Hà Nội là khả năng thi đấu của Nguyễn quang hai Việt Nam')
# ner = NER('học bơi lội và bóng đá nữ turkey')
# print(ner.entities)
