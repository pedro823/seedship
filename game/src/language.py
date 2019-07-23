import json

class LanguageError(Exception):
    pass

class Language:
    AVAIL_LANGS = {
        'pt-BR',
        'en-US'
    }

    LANGUAGE = 'en-US'

    def __init__(self):
        self.language = self.LANGUAGE
        self.txt = self.load_language(self.language)

    def set_language(self, language: str):
        if language not in self.AVAIL_LANGS:
            raise LanguageError(f'{language} is not available. Available languages: {self.AVAIL_LANGS}')
        self.language = language
        self.txt = self.load_language(self.language)

    def load_language(self, language: str) -> dict:
        try:
            with open(f'lang/{language}.json', 'r') as f:
                txt = json.load(f)
            return txt
        except FileNotFoundError:
            raise LanguageError('Could not find language ' + language)

    def __getitem__(self, key):
        return self.txt[key]

TXT = Language()