from django.utils.text import slugify as django_slugify

alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sh', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}


def slugify(s, allow_unicode=False, no_space=False, no_minus=False):
    """
    Overriding django slugify that allows to use russian words as well.
    """
    if no_space:
        alphabet[" "] = "_"
    if no_minus:
        alphabet["-"] = "_"

    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()), allow_unicode)