import os
import docx
import unicodedata
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from subprocess import Popen, PIPE
from web_service_analyzer import settings


class ReadFile(object):
    def __init__(self):
        self.file_system_storage = FileSystemStorage()
        self.media_url = settings.MEDIA_URL
        self.document_path = ""

    def __call__(self, file):
        self.document_path = self.media_url + file.name
        if os.path.exists(self.document_path):
            return HttpResponseRedirect("/index")
        save_file = self.save_file(file)
        text = self.read_text(save_file)
        self.delete_file(save_file)
        return text

    def save_file(self, file):
        filename = self.file_system_storage.save(file.name, file)
        return filename

    def delete_file(self, file):
        os.remove(os.path.join(self.media_url, file))

    def read_text(self, document):
        text = ""
        if document.endswith('.docx'):
            text = self.read_docx()
        elif document.endswith('.doc'):
            text = self.read_doc()
        return text

    def read_docx(self):
        doc = docx.Document(self.document_path)
        text = ' '.join([paragraph.text for paragraph in doc.paragraphs])
        return unicodedata.normalize('NFKD', text)

    def read_doc(self):
        cmd = ['antiword', self.document_path]
        doc = Popen(cmd, stdout=PIPE)
        stdout, stderr = doc.communicate()
        text = stdout.decode('utf-8', 'ignore')
        return text
