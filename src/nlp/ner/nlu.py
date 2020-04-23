"""
Parse entity to NLU
"""

try:
    from nlp.ner.ner_predict import NERPredict
    from utils.pattern.regex_datetime import ner, regex
except ImportError:
    from src.nlp.ner.ner_predict import NERPredict
    from src.utils.pattern.regex_datetime import ner, regex


class NLUPredict:
    """
    Parse entity to NLU
    """

    def __init__(self):
        self.ner = NERPredict()

    def parse_nlu(self, sentence):
        """
        Parse entity to NLU
        5 entity:
            date_start,
            date_stop
            is_country,
            is_name,
            is_sport
        :param sentence:
        :return:
        """
        ngay, thang, nam, hom, thu, tuan, buoi = regex(sentence)
        date_start, date_stop = ner(ngay, thang, nam, hom, tuan, thu, buoi)
        if date_start == 0 and date_stop == 0:
            date_start, date_stop = ner(0, 0, 0, 'hôm nay', None, None, None)
        entities = self.ner.predict(sentence)
        entities['date_start'] = date_start
        entities['date_stop'] = date_stop

        return entities
