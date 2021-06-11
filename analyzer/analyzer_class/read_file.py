import os
from typing import NoReturn
import textract
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
from web_service_analyzer import settings


class ReadFile:
    """
    Класс для чтения данных из файла
    """
    def __init__(self):
        self.media_root = settings.MEDIA_ROOT

    def __call__(self, file):
        filename = self.__save_file(file)
        text = self.__read_text(filename)
        self.__delete_file(filename)
        return text

    @staticmethod
    def __save_file(file: InMemoryUploadedFile) -> str:
        """
        Сохраняет файл
        :param file: файл который приходит в ответе через django
        :return: имя файла
        """
        filename = FileSystemStorage().save(file.name, file)
        return filename

    def __delete_file(self, filename: str) -> NoReturn:
        """
        Удаляет файл из директории media
        :param filename: имя файла
        """
        os.remove(os.path.join(self.media_root, filename))

    def __read_text(self, filename: str) -> str:
        """
        Читает содержимое файла
        :param filename: имя файла
        :return: содержимое файла
        """
        if filename.endswith(('.docx', '.doc', '.txt', '.pdf')):
            return textract.process(os.path.join(self.media_root, filename)).decode('utf-8')
        else:
            return ''



