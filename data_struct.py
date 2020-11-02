import json
import sublime
from .utils import get_file_path_cache

STORAGE_CACHE_NAME = "typing_learn_word"


class BaseDataStruct(object):
    def __init__(self):
        self._storage = {}
        self.read_storage()

    def read_storage(self):
        path = get_file_path_cache(STORAGE_CACHE_NAME)
        try:
            fp = open(path)
            content = fp.read()
            fp.close()
            self._storage = json.loads(content) or {}
        except Exception:
            sublime.error_message("Cann't read local storage data.")

    def save_storage(self):
        path = get_file_path_cache(STORAGE_CACHE_NAME)
        try:
            fp = open(path, "w+")
            fp.write(json.dumps(self._storage))
            fp.close()
        except Exception:
            sublime.error_message("Cann't save local storage data.")


class Book(BaseDataStruct):
    def __init__(self, name):
        super().__init__()

        self.name = name
        if self._storage.get(name) is None:
            self._storage[name] = []

    def add_word(self, word):
        self._storage[self.name].append(word)
        self.save_storage()

    def remove_word(self, word):
        self._storage[self.name].remove(word)
        self.save_storage()

    def remove_all_words(self):
        self._storage[self.name] = []
        self.save_storage()

    def get_words(self):
        return self._storage[self.name]


class BooksManager(BaseDataStruct):
    def __init__(self):
        super().__init__()

    def get_book_list(self):
        return list(self._storage.keys())

    def get_word_by_book_name(self, name):
        return self._storage.get(name, [])
