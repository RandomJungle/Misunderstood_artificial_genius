import re


def phonetize_from_french(string):

    phonetic_string = string.replace('eau', 'o')
    phonetic_string = string.replace('au', 'o')
    phonetic_string = string.replace('ou', 'u')
    phonetic_string = string.replace('', 'o')
    phonetic_string = string.replace('eau', 'o')
    phonetic_string = re.sub('(\w)*?(ay|ai|est)(\w)*?', '\1è\3', string)
    phonetic_string = re.sub('(\w)*?(oi)(\w)*?', '\1wa\3', string)
    return phonetic_string

def phonetize_from_english(string)
    phonetic_string = re.sub('(r|c)ough', 'ruf', string)
    phonetic_string = re.sub('(pl|sl|th|thor)ough(t)?', '\1ow\2', string)
    phonetic_string = re.sub('through', 'thrue', string)
    return phonetic_string