import unittest


def memoize(func):
    cache = {}

    def helper(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return helper


class Rational(object):
    max = None

    def __init__(self, nominator, denominator=1):
        self.nominator = nominator
        self.denominator = denominator
        self._max_rational()

    def __add__(self, other):
        s = Rational(self.nominator * other.denominator + other.nominator * self.denominator,
                     self.denominator * other.denominator)
        return s

    def __sub__(self, other):
        s = Rational(self.nominator * other.denominator - other.nominator * self.denominator,
                     self.denominator * other.denominator)
        return s

    def __mul__(self, other):
        s = Rational(self.nominator * other.nominator, self.denominator * other.denominator)
        return s

    def __truediv__(self, other):
        s = Rational(self.nominator * other.denominator, self.denominator * other.nominator)
        return s

    def __lt__(self, other):
        s = self._create_limited_fraction()
        r = other._create_limited_fraction()
        return True if s.nominator * r.denominator < r.nominator * s.denominator else False

    def __le__(self, other):
        s = self._create_limited_fraction()
        r = other._create_limited_fraction()
        return True if s.nominator * r.denominator <= r.nominator * s.denominator else False

    def __eq__(self, other):
        s = self._create_limited_fraction()
        r = other._create_limited_fraction()
        return True if s.nominator * r.denominator == s.denominator * r.nominator else False

    def __ne__(self, other):
        s = self._create_limited_fraction()
        r = other._create_limited_fraction()
        return True if s.nominator != r.nominator or s.denominator != r.denominator else False

    def __gt__(self, other):
        s = self._create_limited_fraction()
        r = other._create_limited_fraction()
        return True if s.nominator * r.denominator > r.nominator * s.denominator else False

    def __ge__(self, other):
        s = self._create_limited_fraction()
        r = other._create_limited_fraction()
        return True if s.nominator * r.denominator >= s.nominator * r.denominator else False

    def __str__(self):
        self._create_limited_fraction()
        return "%d/%d" % (self.nominator, self.denominator)

    def __repr__(self):
        self._create_limited_fraction()
        return "%s(%r, %r)" % (self.__class__.__name__, self.nominator, self.denominator)

    def _gcd(self):
        n = self.nominator
        d = self.denominator
        while d != 0:
            (n, d) = (d, n % d)
        return n

    def _create_limited_fraction(self):
        s = self._gcd()
        self.nominator //= s
        self.denominator //= s
        return self

    def _max_rational(self):
        if Rational.max is None:
            Rational.max = self
        else:
            if self > Rational.max:
                Rational.max = self
        return Rational.max


def myZip(iterable1, iterable2, fill=None):
    it1 = iter(iterable1)
    it2 = iter(iterable2)
    i = next(it1, None)
    j = next(it2, None)
    while i is not None or j is not None:
        result = []
        if i is None:
            if fill is not None:
                result.append(fill)
            else:
                break
        else:
            result.append(i)
        i = next(it1, None)
        if j is None:
            if fill is not None:
                result.append(fill)
            else:
                break
        else:
            result.append(j)
        j = next(it2, None)
        yield tuple(result)


class MyZip(object):
    def __init__(self, iterable1, iterable2, fill=None):
        self.iterable1 = iterable1
        self.iterable2 = iterable2
        self.fill = fill

    def __iter__(self):
        return MyZip.MyZipIterator(iter(self.iterable1), iter(self.iterable2), self.fill)

    class MyZipIterator(object):

        def __init__(self, it1, it2, fill):
            self.it1 = it1
            self.it2 = it2
            self.fill = fill
            self.a = next(it1, None)
            self.b = next(it2, None)

        def __iter__(self):
            return self

        def __next__(self):
            if self.a is not None and self.b is not None:
                s, r = self.a, self.b
                self.a = next(self.it1, None)
                self.b = next(self.it2, None)
                return s, r

            if self.fill is not None:
                if self.a is not None and self.b is None:
                    s = self.a
                    self.a = next(self.it1, None)
                    return s, self.fill

                elif self.a is None and self.b is not None:
                    s = self.b
                    self.b = next(self.it2, None)
                    return self.fill, s
            raise StopIteration


def is_anagram(word, words_file):
    str1 = sorted(word)
    str2 = sorted(words_file)
    return True if str1 == str2 else False


def anagram(word):
    my_anagrams = []
    file = open("words.txt", 'r')
    words_file = file.readline().strip()
    while words_file != "":
        words_file = file.readline().strip()
        is_it = is_anagram(word, words_file)
        if is_it is True:
            my_anagrams.append(words_file)
    file.close()
    return my_anagrams


class VariableDescriptor:
    def __init__(self):
        self.value = 0

    def __get__(self, instance, owner):
        instance._readCount = instance._readCount + 1
        return self.value

    def __set__(self, instance, value):
        self.value = value
        instance.history().append(value)
        instance._writeCount = instance._writeCount + 1


class Variable:
    value = VariableDescriptor()
    _writeCount = 0
    _readCount = 0

    def __init__(self, value):
        self._history = []
        self._value = value
        self.value = value

    def writeCount(self):
        return self._writeCount

    def readCount(self):
        return self._readCount

    def history(self):
        return self._history


class MyTest(unittest.TestCase):
    def test_memoize(self):
        count = 0

        @memoize
        def my_sum(x, y):
            nonlocal count
            count += 1
            return x + y

        @memoize
        def my_mul(x, y):
            print('calling mul')
            return x * y

        my_sum(3, 2)
        self.assertEqual(count, 1)
        my_sum(3, 2)
        self.assertEqual(count, 1)
        my_sum(4, 2)
        self.assertEqual(count, 2)
        my_sum(3, 2)
        self.assertEqual(count, 2)

    def test_Rational(self):
        half = Rational(5, 10)
        third = Rational(8, 24)
        self.assertEqual(half.__str__(), '1/2')
        self.assertEqual(half.__repr__(), 'Rational(1, 2)')
        self.assertEqual(Rational.max, Rational(1, 2))
        self.assertEqual(third.__str__(), '1/3')
        self.assertEqual(half + third, Rational(5, 6))
        self.assertEqual(third - half, Rational(-1, 6))
        self.assertEqual(half * third, Rational(1, 6))
        self.assertEqual(half / third, Rational(3, 2))
        self.assertEqual(half == third, False)
        self.assertEqual(half != third, True)
        self.assertEqual(half < third, False)
        self.assertEqual(half <= third, False)
        self.assertEqual(half > third, True)
        self.assertEqual(half >= third, True)
        self.assertEqual(Rational.max, Rational(3 / 2))
        two = Rational(2)
        self.assertEqual(two.__repr__(), 'Rational(2, 1)')

    def test_myZip(self):
        g = (3 * i for i in range(5))
        my_list = list(myZip(g, ["a", "b", "c"], fill="bye"))
        self.assertEqual(my_list, [(0, "a"), (3, "b"), (6, "c"), (9, "bye"), (12, "bye")])

        my_list = list(myZip(["a", "b", "c"], [1, 2, 3, 4], fill="bye"))
        self.assertEqual(my_list, [("a", 1), ("b", 2), ("c", 3), ("bye", 4)])

        my_list = list(myZip(["a", "b", "c"], [1, 2, 3], fill="bye"))
        self.assertEqual(my_list, [("a", 1), ("b", 2), ("c", 3)])

        my_list = list(myZip([], [], fill="bye"))
        self.assertEqual(my_list, [])

        my_list = list(myZip(["a", "b"], [1, 2, 3]))
        self.assertEqual(my_list, [("a", 1), ("b", 2)])

    def test_MyZip(self):
        my_list = list(MyZip([1, 2, 3], ["a", "b", "c"], "bye"))
        self.assertEqual(my_list, [(1, "a"), (2, "b"), (3, "c")])

        my_list = list(MyZip([1, 2], ["a", "b", "c"], "bye"))
        self.assertEqual(my_list, [(1, "a"), (2, "b"), ("bye", "c")])

        my_list = list(MyZip([1, 2, 3], ["a", "b"], "bye"))
        self.assertEqual(my_list, [(1, "a"), (2, "b"), (3, "bye")])

        my_list = list(MyZip([], [], fill="bye"))
        self.assertEqual(my_list, [])

        my_list = list(MyZip(["a", "b"], [1, 2, 3]))
        self.assertEqual(my_list, [("a", 1), ("b", 2)])

    def test_anagram(self):
        self.assertEqual(anagram('restful'), ['fluster', 'fluters', 'restful'])
        self.assertEqual(anagram('rrao'), ['orra', 'roar'])
        self.assertEqual(anagram('sariel'), ['ariels', 'resail', 'sailer', 'serail', 'serial'])
        self.assertEqual(anagram('binyamin'), [])

    def test_Variable(self):
        v = Variable(30)
        self.assertEqual(v.history(), [30])
        self.assertEqual(v.readCount(), 0)
        self.assertEqual(v.writeCount(), 1)
        v.value
        self.assertEqual(v.readCount(), 1)


if __name__ == '__main__':
    unittest.main()
