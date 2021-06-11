from collections import OrderedDict
from typing import Dict, Union

from django.core.files.uploadedfile import InMemoryUploadedFile
from analyzer.analyzer_class.read_file import ReadFile
from analyzer.analyzer_class.singleton_meta import SingletonMeta
from analyzer.analyzer_class.text_preprocessing import TextPreprocessing
from analyzer.analyzer_class.tf_idf import compute_tfidf


class Thesaurus(metaclass=SingletonMeta):
    """
    Класс для определения тезауруса и TF-IDF текста
    """
    def __init__(self):
        self.__text_preprocessing = TextPreprocessing()
        self.__read_file = ReadFile()
        # значения для закона Хипса
        self.alpha = 15
        self.betta = 1.7

    def __call__(self, text: Union[str, InMemoryUploadedFile]) -> Dict[str, float]:
        text = self.__retrieve_text(text)
        if not text:
            return {}
        clean_sentences = self.__text_preprocessing(text)
        tfidf_dict = compute_tfidf(clean_sentences)
        n = self.__get_n(len(tfidf_dict))
        tfidf_dict = self.__get_thesaurus_range(tfidf_dict, n)
        return tfidf_dict

    def __get_n(self, number_of_all_words: int) -> int:
        """
        Определяет сколько слов нужно взять в тезаурус
        :param number_of_all_words: число отобранных слов
        :return: число слов
        """
        return round(pow(number_of_all_words/self.alpha, 1/self.betta))

    @staticmethod
    def __get_thesaurus_range(dictionary: Dict[str, float], n: int) -> Dict[str, float]:
        """
        Возвращает словарь с n первыми значениями
        :param dictionary: словарь
        :param n: сколько значений оставить
        :return: результирующий словарь
        """
        new_dict = OrderedDict()
        for key in list(dictionary.keys())[0:n]:
            new_dict[key] = dictionary[key]
        return new_dict

    def __retrieve_text(self, text: Union[str, InMemoryUploadedFile]) -> str:
        """
        Обрабатывает входной параметр. Если это файл, то считывает текст оттуда.
        :param text:
        :return:
        """
        if type(text) is str:
            return text
        elif type(text) is InMemoryUploadedFile:
            return self.__read_file(text)

