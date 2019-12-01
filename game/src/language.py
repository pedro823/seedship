import json
import os
import sys

class LanguageError(Exception):
    pass

class Language:
    AVAIL_LANGS = [language.rstrip('.json') for language in os.listdir('lang/')]
    DEFAULT_LANGUAGE = 'en-US'

    def __init__(self):
        self.language = self.DEFAULT_LANGUAGE
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

    def prompt_available_languages(self):
        print('Available languages:')
        for index, language in enumerate(self.AVAIL_LANGS):
            print(f'{index}    {language}')

        while True:
            try:
                language_choice = int(input(f'select language [0 - {len(self.AVAIL_LANGS) - 1}]: '))
                if 0 <= language_choice < len(self.AVAIL_LANGS):
                    self.language = self.AVAIL_LANGS[language_choice]
                    self.txt = self.load_language(self.language)
                    break
            except EOFError:
                sys.exit(1)
            except json.JSONDecodeError as e:
                print(f'Error parsing language file: {e}')
            except:
                continue


    def __getitem__(self, key):
        return self.txt[key]

TXT = Language()