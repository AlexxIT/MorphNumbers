from pymorphy2 import MorphAnalyzer

from custom_components.morph_numbers import MorphNumber

morph = MorphNumber()


def test_numword():
    assert morph.numword(1, "градус") == "один градус"
    assert morph.numword(1, "задача") == "одна задача"
    assert morph.numword(1, "дерево") == "одно дерево"

    s = morph.numword(2000435, "синее облако")
    assert s == "два миллиона четыреста тридцать пять синих облаков"

    s = morph.numword(2, "запланированная задача", False)
    assert s == "2 запланированные задачи"

    s = morph.numword(5, "просроченная задача", False)
    assert s == "5 просроченных задач"

    assert morph.numword(123) == "сто двадцать три"

    # https://github.com/AlexxIT/MorphNumbers/issues/1
    assert morph.numword(0, "градус") == "ноль градусов"
    assert morph.numword(-2, "градус") == "минус два градуса"


def test_second():
    # https://github.com/AlexxIT/MorphNumbers/issues/3
    assert morph.numword(31, "секунда") == "тридцать одна секунда"
    assert morph.numword(31, "секунду") == "тридцать одну секунду"


def test_ordional():
    # https://github.com/AlexxIT/MorphNumbers/issues/11
    assert morph.ordinal_number(100, "первому") == "сотому"
    assert morph.ordinal_number(3, "первое") == "третье"


def test_vatt():
    # https://github.com/AlexxIT/MorphNumbers/issues/12
    assert morph.numword(1, "ватт") == "один ватт"
    assert morph.numword(2, "ватт") == "два ватта"
    assert morph.numword(22, "ватт") == "двадцать два ватта"
    assert morph.numword(92, "ватт") == "девяносто два ватта"


def test_float():
    # https://github.com/AlexxIT/MorphNumbers/issues/13
    assert morph.numword(8.0, "первого") == "восемь первых"
    assert morph.ordinal_number(8.0, "первого") == "восьмого"


def test_reverse():
    assert morph.reverse("один") == 1
    assert morph.reverse("одна") == 1
    assert morph.reverse("одно") == 1
    assert morph.reverse("первый") == 1
    assert morph.reverse("первая") == 1
    assert morph.reverse("первое") == 1

    assert morph.reverse("сто двадцать три") == 123

    assert morph.reverse("два миллиона четыреста тридцать пять") == 2000435

    n = morph.reverse("девятьсот восемьдесят семь тысяч шестьсот пятьдесят четыре")
    assert n == 987654


def test_kilogramm():
    # https://github.com/AlexxIT/MorphNumbers/issues/18
    assert morph.words_with_number(10, "килограмм") == ["килограммов"]
    assert morph.words_with_number(10, "стол") == ["столов"]


def test_may():
    assert morph.words_with_number(5, "май") == []


def test_integrations():
    s = morph.custom_numword(3, ["интеграция", "интеграции", "интеграций"])
    assert s == "три интеграции"

    s = morph.custom_numword(3, ["интеграция", "интеграции", "интеграций"], False)
    assert s == "3 интеграции"
