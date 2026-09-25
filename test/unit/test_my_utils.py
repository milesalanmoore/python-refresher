"""Unit tests for my_utils.

Run from the repository root with:
    python -m unittest discover -s test/unit
"""
import os
import random
import statistics
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
import my_utils  # noqa: E402

N_RANDOM_TRIALS = 100


def random_int_list(min_length=1, max_length=100):
    """Return a list of random integers with a random length.

    Parameters
    ----------
    min_length : int, optional
        Shortest list to return.
    max_length : int, optional
        Longest list to return.

    Returns
    -------
    list of int
        Integers drawn uniformly from -1000 to 1000.
    """
    length = random.randint(min_length, max_length)
    return [random.randint(-1000, 1000) for _ in range(length)]


def write_csv(rows):
    """Write rows to a temporary CSV file and return its path.

    Parameters
    ----------
    rows : list of list of str
        Rows to write, the first of which is the header.

    Returns
    -------
    str
        Path to the file. The caller is responsible for removing it.
    """
    with tempfile.NamedTemporaryFile('w', suffix='.csv',
                                     delete=False) as f:
        for row in rows:
            f.write(','.join(row) + '\n')
    return f.name


class TestGetMean(unittest.TestCase):

    def test_known_values(self):
        self.assertEqual(my_utils.get_mean([1, 2, 3, 4]), 2.5)
        self.assertEqual(my_utils.get_mean([-5]), -5)

    def test_random_lists(self):
        for _ in range(N_RANDOM_TRIALS):
            values = random_int_list()
            self.assertAlmostEqual(my_utils.get_mean(values),
                                   statistics.mean(values))

    def test_random_constant_list(self):
        value = random.randint(-1000, 1000)
        values = [value] * random.randint(1, 100)
        self.assertEqual(my_utils.get_mean(values), value)

    def test_empty_list(self):
        with self.assertRaises(ValueError):
            my_utils.get_mean([])

    def test_non_numeric(self):
        with self.assertRaises(TypeError):
            my_utils.get_mean(['a', 'b'])


class TestGetMedian(unittest.TestCase):

    def test_known_values(self):
        self.assertEqual(my_utils.get_median([3, 1, 2]), 2)
        self.assertEqual(my_utils.get_median([4, 1, 3, 2]), 2.5)

    def test_random_lists(self):
        for _ in range(N_RANDOM_TRIALS):
            values = random_int_list()
            self.assertAlmostEqual(my_utils.get_median(values),
                                   statistics.median(values))

    def test_random_order_does_not_matter(self):
        values = random_int_list()
        shuffled = random.sample(values, len(values))
        self.assertEqual(my_utils.get_median(values),
                         my_utils.get_median(shuffled))

    def test_input_not_modified(self):
        values = random_int_list()
        original = list(values)
        my_utils.get_median(values)
        self.assertEqual(values, original)

    def test_empty_list(self):
        with self.assertRaises(ValueError):
            my_utils.get_median([])

    def test_non_numeric(self):
        with self.assertRaises(TypeError):
            my_utils.get_median([1, 'b'])


class TestGetStd(unittest.TestCase):

    def test_known_values(self):
        self.assertEqual(my_utils.get_std([2, 4, 4, 4, 5, 5, 7, 9]), 2)
        self.assertEqual(my_utils.get_std([7]), 0)

    def test_random_lists(self):
        for _ in range(N_RANDOM_TRIALS):
            values = random_int_list()
            self.assertAlmostEqual(my_utils.get_std(values),
                                   statistics.pstdev(values))

    def test_random_constant_list(self):
        values = [random.randint(-1000, 1000)] * random.randint(1, 100)
        self.assertEqual(my_utils.get_std(values), 0)

    def test_random_shift_does_not_change_std(self):
        values = random_int_list(min_length=2)
        shift = random.randint(-1000, 1000)
        shifted = [value + shift for value in values]
        self.assertAlmostEqual(my_utils.get_std(values),
                               my_utils.get_std(shifted))

    def test_empty_list(self):
        with self.assertRaises(ValueError):
            my_utils.get_std([])

    def test_non_numeric(self):
        with self.assertRaises(TypeError):
            my_utils.get_std(['a', 'b'])


class TestResolveColumn(unittest.TestCase):

    def setUp(self):
        self.headers = ['Area', 'Year', 'Savanna fires']

    def test_name(self):
        self.assertEqual(my_utils.resolve_column(self.headers, 'Year'), 1)

    def test_random_index(self):
        index = random.randrange(len(self.headers))
        self.assertEqual(my_utils.resolve_column(self.headers, index),
                         index)

    def test_unknown_name(self):
        with self.assertRaises(ValueError):
            my_utils.resolve_column(self.headers, 'Country')

    def test_index_out_of_range(self):
        with self.assertRaises(ValueError):
            my_utils.resolve_column(self.headers, len(self.headers))
        with self.assertRaises(ValueError):
            my_utils.resolve_column(self.headers, -1)


class TestGetColumn(unittest.TestCase):

    def setUp(self):
        # Random values for two countries, interleaved in random order
        self.a_values = [float(v) for v in random_int_list()]
        self.b_values = [float(v) for v in random_int_list()]
        rows = ([['A', str(v)] for v in self.a_values]
                + [['B', str(v)] for v in self.b_values])
        random.shuffle(rows)
        self.expected_a = [float(r[1]) for r in rows if r[0] == 'A']
        self.file_name = write_csv([['Area', 'Value']] + rows)

    def tearDown(self):
        os.remove(self.file_name)

    def test_random_values_by_name(self):
        result = my_utils.get_column(self.file_name, 'Area', 'A',
                                     result_column='Value')
        self.assertEqual(result, self.expected_a)

    def test_random_values_by_index(self):
        result = my_utils.get_column(self.file_name, 0, 'A',
                                     result_column=1)
        self.assertEqual(result, self.expected_a)

    def test_no_match(self):
        result = my_utils.get_column(self.file_name, 'Area', 'C',
                                     result_column='Value')
        self.assertEqual(result, [])

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            my_utils.get_column(self.file_name + '.missing', 'Area', 'A')

    def test_empty_file(self):
        empty_file = write_csv([])
        try:
            with self.assertRaises(ValueError):
                my_utils.get_column(empty_file, 'Area', 'A')
        finally:
            os.remove(empty_file)

    def test_bad_column(self):
        with self.assertRaises(ValueError):
            my_utils.get_column(self.file_name, 'Country', 'A')

    def test_non_numeric_result(self):
        with self.assertRaises(ValueError):
            my_utils.get_column(self.file_name, 'Area', 'A',
                                result_column='Area')


if __name__ == '__main__':
    unittest.main()
