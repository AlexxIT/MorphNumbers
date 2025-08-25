from custom_components.morph_numbers import MorphNumber

morph = MorphNumber()


def test_numword():
    assert morph.number_with_text(1, "градус") == "один градус"
    assert morph.number_with_text(1, "задача") == "одна задача"
    assert morph.number_with_text(1, "дерево") == "одно дерево"

    assert morph.number_with_text(2, "градус") == "два градуса"
    assert morph.number_with_text(2, "задача") == "две задачи"
    assert morph.number_with_text(2, "дерево") == "два дерева"

    assert morph.number_with_text(1, "грамм") == "один грамм"
    assert morph.number_with_text(2, "грамм") == "два грамма"
    assert morph.number_with_text(5, "грамм") == "пять граммов"

    assert (
        morph.number_with_text(2000435, "синее облако")
        == "два миллиона четыреста тридцать пять синих облаков"
    )

    assert (
        morph.number_with_text(2, "запланированная задача", as_text=False)
        == "2 запланированные задачи"
    )

    assert (
        morph.number_with_text(5, "просроченная задача", as_text=False)
        == "5 просроченных задач"
    )

    assert morph.number_with_text(123, "") == "сто двадцать три"

    # https://github.com/AlexxIT/MorphNumbers/issues/1
    assert morph.number_with_text(0, "градус") == "ноль градусов"
    assert morph.number_with_text(-2, "градус") == "минус два градуса"


def test_second():
    # https://github.com/AlexxIT/MorphNumbers/issues/3
    assert morph.number_with_text(31, "секунда") == "тридцать одна секунда"
    assert morph.number_with_text(31, "секунду") == "тридцать одну секунду"


def test_ordional():
    # https://github.com/AlexxIT/MorphNumbers/issues/11
    assert morph.number_to_ordinal(100, "первому") == "сотому"
    assert morph.number_to_ordinal(3, "первое") == "третье"

    # https://github.com/AlexxIT/MorphNumbers/issues/13
    assert morph.number_to_ordinal(8.0, "первого") == "восьмого"


def test_eleventh():
    # https://github.com/AlexxIT/MorphNumbers/issues/31
    assert morph.number_to_ordinal(11, "первого") == "одиннадцатого"


def test_vatt():
    # https://github.com/AlexxIT/MorphNumbers/issues/12
    assert morph.number_with_text(1, "ватт") == "один ватт"
    assert morph.number_with_text(2, "ватт") == "два ватта"
    assert morph.number_with_text(22, "ватт") == "двадцать два ватта"
    assert morph.number_with_text(92, "ватт") == "девяносто два ватта"


def test_reverse():
    assert morph.text_to_integer("один") == 1
    assert morph.text_to_integer("одна") == 1
    assert morph.text_to_integer("одно") == 1
    assert morph.text_to_integer("первый") == 1
    assert morph.text_to_integer("первая") == 1
    assert morph.text_to_integer("первое") == 1

    assert morph.text_to_integer("сто двадцать три") == 123

    assert morph.text_to_integer("два миллиона четыреста тридцать пять") == 2000435

    assert (
        morph.text_to_integer(
            "девятьсот восемьдесят семь тысяч шестьсот пятьдесят четыре"
        )
        == 987654
    )


def test_kilogramm():
    # https://github.com/AlexxIT/MorphNumbers/issues/18
    assert morph.words_after_number(10, "килограмм") == ["килограммов"]
    assert morph.words_after_number(10, "стол") == ["столов"]


def test_may():
    assert morph.words_after_number(5, "май") == []


def test_integrations():
    assert (
        morph.number_with_custom_text(3, ["интеграция", "интеграции", "интеграций"])
        == "три интеграции"
    )

    assert (
        morph.number_with_custom_text(
            3, ["интеграция", "интеграции", "интеграций"], as_text=False
        )
        == "3 интеграции"
    )

    assert (
        morph.number_with_custom_text(2, ["грамм", "грамма", "граммов"]) == "два грамма"
    )


def test_float():
    assert (
        morph.number_with_text(21.1, "градус")
        == "двадцать одна целая и одна десятая градуса"
    )
    assert (
        morph.number_with_text(22.2, "градус")
        == "двадцать две целых и две десятых градуса"
    )
    assert (
        morph.number_with_text(22.09, "градус")
        == "двадцать две целых и девять сотых градуса"
    )
    assert (
        morph.number_with_text(22.009, "градус")
        == "двадцать две целых и девять тысячных градуса"
    )

    assert (
        morph.number_with_text(22.9876, "градус")
        == "двадцать две целых и девятьсот восемьдесят восемь тысячных градуса"
    )

    assert (
        morph.number_with_text(11.11, "градус")
        == "одиннадцать целых и одиннадцать сотых градуса"
    )

    assert (
        morph.number_with_text(111.111, "градус")
        == "сто одиннадцать целых и сто одиннадцать тысячных градуса"
    )

    assert (
        morph.number_with_text(21.1, "яркость")
        == "двадцать одна целая и одна десятая яркости"
    )
    assert (
        morph.number_with_text(22.2, "яркость")
        == "двадцать две целых и две десятых яркости"
    )


def test_case():
    # Кто? Что?
    assert morph.number_with_text(1, "муниципальный") == "один муниципальный"
    # Кого? Чего?
    assert morph.number_with_text(1, "муниципального") == "одного муниципального"
    # Кому? Чему?
    assert morph.number_with_text(1, "муниципальному") == "одному муниципальному"
    # Кого? Что?
    assert morph.number_with_text(1, "муниципального") == "одного муниципального"
    # Кем? Чем?
    assert morph.number_with_text(1, "муниципальным") == "одним муниципальным"
    # О ком? О чём?
    assert morph.number_with_text(1, "муниципальном") == "одном муниципальном"

    assert morph.number_with_text(2, "муниципальном") == "два муниципальных"
    assert morph.number_with_text(5, "муниципальном") == "пять муниципальных"
    assert morph.number_with_text(21, "муниципальном") == "двадцать одном муниципальном"
