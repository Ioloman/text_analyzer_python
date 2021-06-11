from typing import List


def calculate_compatibility(one_keys: List[str], two_keys: List[str]) -> int:
    """
    Определяет процентную совместимость двух текстов
    :param one_keys: тезаурус одного текста
    :param two_keys: тезаурус второго текста
    :return: процент
    """
    if not one_keys or not two_keys:
        return 0
    common_keywords = 0
    for word in two_keys:
        if word in one_keys:
            common_keywords += 1
    return round(common_keywords / min(len(one_keys), len(two_keys))*100)

