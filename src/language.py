import json

AVAIL_LANGS = (
    'pt-BR'
    'en-US'
)

LANGUAGE = 'pt-BR'


class LanguageError(Exception):
    pass


def load_language(language: str) -> dict:
    try:
        with open(f'lang/{language}.json', 'r') as f:
            lang_dict = json.load(f)
        return lang_dict
    except FileNotFoundError:
        raise LanguageError('Could not find language ' + language)


TXT = LANG_DICT = load_language(LANGUAGE)
