import json

AVAIL_LANGS = (
    'pt-BR'
)

LANGUAGE = 'pt-BR'

class LanguageError(Exception):
    pass

def load_language(language: str):
    try:
        with open('langs/' + language, 'r') as f:
            lang_dict = json.load(f)
        return lang_dict
    except FileNotFoundError:
        raise LanguageError('Could not find language ' + language)

TXT = LANG_DICT = load_language(LANGUAGE)
