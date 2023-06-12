import inspect

from pymorphy2 import MorphAnalyzer
from pymorphy2.analyzer import Parse

NUMBERS = """0,ноль,нулевой
1,один,первый
2,два,второй
3,три,третий
4,четыре,четвертый
5,пять,пятый
6,шесть,шестой
7,семь,седьмой
8,восемь,восьмой
9,девять,девятый
10,десять,десятый
11,одинадцать,одинадцатый
12,двенадцать,двенадцатый
13,тринадцать,тринадцатый
14,четырнадцать,четырнадцатый
15,пятнадцать,пятнадцатый
16,шестнадцать,шестнадцатый
17,семнадцать,семнадцатый
18,восемнадцать,восемнадцатый
19,девятнадцать,девятнадцатый
20,двадцать,двадцатый
30,тридцать,тридцатый
40,сорок,сороковой
50,пятьдесят,пятидесятый
60,шестьдесят,шестидесятый
70,семьдесят,семидесятый
80,восемьдесят,восьмидесятый
90,девяносто,девяностый
100,сто,сотый
200,двести,двухсотый
300,триста,трехсотый
400,четыреста,четырехсотый
500,пятьсот,пятисотый
600,шестьсот,шестисотый
700,семьсот,семисотый
800,восемьсот,восьмисотый
900,девятьсот,девятисотый
1000,тысяча,тысячный
1000000,миллион,миллионный"""

# fix Python 3.11 support
if not hasattr(inspect, "getargspec"):

    def getargspec(*args):
        spec = inspect.getfullargspec(*args)
        return spec.args, spec.varargs, spec.varkw, spec.defaults

    inspect.getargspec = getargspec


class MorphNumber:
    def __init__(self):
        morph = MorphAnalyzer()
        self.parse = lambda word: morph.parse(word)[0]

        # создаём словарь из чисел и порядковых числительных
        self.dict = {}
        for i in NUMBERS.split("\n"):
            x, card, ord_ = i.split(",")
            self.dict[int(x)] = card
            self.dict[card] = ord_

    def number_to_words(self, number: int, text: str = None) -> list:
        """Конвертирует число в текст, опционально согласуя его с текстом после
        числа. Поддерживает только целые числа
        """
        if number < 0:
            return ["минус"] + self.number_to_words(-number, text)

        if number == 0:
            return [self.dict[number]]

        # граммемы последней цифры
        if text:
            word = text.rsplit(" ", 1)[-1]
            tag = self.parse(word).tag
        else:
            tag = None

        hundred = 0
        ten = 0
        words = []

        # номер цифры в числе
        k = len(str(number)) - 1
        for digit in str(number):
            digit = int(digit)

            # сотни
            if k % 3 == 2:
                if digit > 0:
                    words.append(self.dict[digit * 100])
                hundred = digit

            # десятки
            elif k % 3 == 1:
                if digit > 1:
                    words.append(self.dict[digit * 10])
                ten = digit

            # тысячи и единицы
            else:
                # десять, одинадцать, двенадцать...
                if ten == 1:
                    digit += 10

                if digit > 0:
                    # тысячи женского рода (только для 1 и 2)
                    # например: одна тысяча, две тысячи
                    if k == 3 and digit <= 2:
                        w: Parse = self.parse(self.dict[digit])
                        w: Parse = w.inflect({"femn"})
                        words.append(w.word)

                    # граммемы последней цифры (только для 1 и 2)
                    # например: один градус, одна задача, одно дерево
                    elif k == 0 and digit <= 2 and tag:
                        w: Parse = self.parse(self.dict[digit])
                        w: Parse = w.inflect({tag.gender, tag.case})
                        words.append(w.word)

                    else:
                        words.append(self.dict[digit])

                # например: сто тысяч, десять миллионов, один миллиард
                if k > 2 and (hundred or ten or digit):
                    w2: Parse = self.parse(self.dict[10**k])
                    w2: Parse = w2.make_agree_with_number(digit)
                    words.append(w2.word)

            k -= 1

        return words

    def ordinal_number(self, number: Union[int, float, str], first_word: str):
        if number >= 1000:
            return str(number)

        # число всегда конвертируется в целое
        number = int(float(number))

        words = self.number_to_words(number)
        last_word = words.pop()

        ordinal = self.dict[last_word]
        w: Parse = self.parse(ordinal)

        tag = self.parse(first_word).tag
        w: Parse = w.inflect({tag.gender, tag.case})

        return " ".join(words + [w.word])

    def words_with_number(self, number: int, text: str):
        number = abs(number)
        words = []
        for word in text.split(" "):
            w: Parse = self.parse(word)
            w: Parse = w.make_agree_with_number(number)
            # 5|format(morph='май') => None
            if w:
                words.append(w.word)
        return words

    def numword(self, number, text: str = None, as_text: bool = True):
        # число всегда конвертируется в целое
        number = int(float(number))

        # as_text=True выведет число в виде строки
        if as_text is True:
            words = self.number_to_words(number, text)
        # as_text=True выведет число в виде числа
        elif as_text is False:
            words = [str(number)]
        # as_text=None не выведет число вообще
        else:
            words = []

        if text:
            words += self.words_with_number(number, text)

        return " ".join(words)

    def custom_numword(self, number, text: list, as_text: bool = True):
        # число всегда конвертируется в целое
        number = int(float(number))

        if (number % 10 == 1) and (number % 100 != 11):
            text = text[0]
        elif (
            (number % 10 >= 2)
            and (number % 10 <= 4)
            and (number % 100 < 10 or number % 100 >= 20)
        ):
            text = text[1]
        else:
            text = text[2]

        # as_text=True выведет число в виде строки
        if as_text is True:
            words = self.number_to_words(number, text)
        # as_text=True выведет число в виде числа
        elif as_text is False:
            words = [str(number)]
        # as_text=None не выведет число вообще
        else:
            words = []

        return " ".join(words + [text])

    def reverse(self, text: str) -> int:
        result = 0

        for word in re.findall("[а-я]+", text):
            # 1. Get normal form
            w: Parse = self.parse(word)
            word = w.normal_form

            # 2. Check word in dict
            numb = next((k for k, v in self.dict.items() if v == word), None)
            if numb is None:
                continue

            # 3. Check word is ordional
            if isinstance(numb, str):
                numb = next((k for k, v in self.dict.items() if v == numb), None)

            # 4. Check word is a thousand or a million
            if numb >= 1000:
                result *= numb
                continue

            result += numb

        return result
