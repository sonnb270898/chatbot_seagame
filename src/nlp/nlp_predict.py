"""
Get NLU, Intent of sentence
"""
import unicodedata

try:
    from utils.logger import log_debug
    from nlp.ner.nlu import NLUPredict
    from nlp.intent.svm_model import SVMModel
except ImportError:
    from src.utils.logger import log_debug
    from src.nlp.ner.nlu import NLUPredict
    from src.nlp.intent.svm_model import SVMModel


class NLPPredictor:
    """
    Get NLU, Intent of sentence
    """

    def __init__(self):
        self.nlu = NLUPredict()
        self.intent = SVMModel()

    def get_snips(self, sentence):
        """
        get snips in sentence
        :param sentence: str
        :return:
        {
            "intent": "schedule",
            "sentence": "lịch thi đấu ngày mai",
            "entity": {
                date_start: ngay mai
            }
        }
        """
        res = dict()
        log_debug('############# PREPROCESSING ##############')
        sentence = unicodedata.normalize("NFC", sentence.lower())
        log_debug("Sentence after preprocessing: {}".format(sentence))

        log_debug('############# NER ##############')
        entity = self.nlu.parse_nlu(sentence)
        log_debug("Entity: {}".format(entity))

        sentence = sentence.replace(entity["is_name"][0], 'vận động viên') if entity[
            "is_name"] else sentence

        sentence = sentence.replace(entity["is_name"][0], entity["is_name"][0] + ' bộ môn') if \
            entity["is_name"] else sentence

        log_debug('############# CLASSIFICATION ##############')
        intent = self.intent.predict(sentence, entity)
        log_debug("Intent: {}".format(intent))

        res["sentence"] = sentence
        res["entity"] = entity
        res["intent"] = intent
        return res
