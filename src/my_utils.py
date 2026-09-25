"""Utilities for pulling numeric columns out of a CSV file.

* get_column - return the values of one column where another column matches
* get_mean - return the arithmetic mean of a non-empty list of numbers
* get_median - return the median of a non-empty list of numbers
* get_std - return the population standard deviation of a list of numbers
"""
import math


def resolve_column(headers, column):
    """Turn a column index or header name into a column index.

    Parameters
    ----------
    headers : list of str
        Header fields from the first line of the file.
    column : int or str
        Zero-based column index, or the name of a header field.

    Returns
    -------
    int
        Zero-based index of the column.

    Raises
    ------
    ValueError
        If the name is not in headers, or the index is out of range.
    """
    if isinstance(column, int):
        if column < 0 or column >= len(headers):
            raise ValueError('Column index ' + str(column)
                             + ' is out of range for a file with '
                             + str(len(headers)) + ' columns')
        return column

    try:
        return headers.index(column)
    except ValueError:
        raise ValueError('Column "' + str(column)
                         + '" is not a header in this file')


def get_column(file_name, query_column, query_value, result_column=1):
    """Get the numeric values of one column where another column matches.

    Parameters
    ----------
    file_name : str
        Path to a comma-separated file whose first line holds the headers.
    query_column : int or str
        Column to match against, as an index or a header name.
    query_value : str
        Value that query_column must equal for a row to be included.
    result_column : int or str, optional
        Column whose values are returned, as an index or a header name.

    Returns
    -------
    list of float
        Values of result_column for every matching row, in file order.

    Raises
    ------
    FileNotFoundError
        If file_name does not exist.
    PermissionError
        If file_name cannot be read.
    ValueError
        If a column cannot be resolved, or a matched value is not numeric.
    """
    with open(file_name, 'r') as f:
        lines = f.readlines()

    if not lines:
        raise ValueError(file_name + ' is empty')

    headers = lines[0].strip().split(',')
    query_idx = resolve_column(headers, query_column)
    result_idx = resolve_column(headers, result_column)

    result = []
    for line in lines[1:]:
        values = line.strip().split(',')
        if len(values) <= max(query_idx, result_idx):
            continue
        if values[query_idx] != query_value:
            continue
        try:
            result.append(float(values[result_idx]))
        except ValueError:
            raise ValueError('Could not convert "' + values[result_idx]
                             + '" in column ' + headers[result_idx]
                             + ' to a number')

    return result


def check_not_empty(values):
    """Raise an error if a list of numbers is empty.

    Parameters
    ----------
    values : list of int or float
        Numbers to check.

    Raises
    ------
    ValueError
        If values is empty.
    """
    if len(values) == 0:
        raise ValueError('Cannot summarize an empty list of values')


def get_mean(values):
    """Compute the arithmetic mean of a list of numbers.

    Parameters
    ----------
    values : list of int or float
        Non-empty list of numbers.

    Returns
    -------
    float
        Arithmetic mean of values.

    Raises
    ------
    ValueError
        If values is empty.
    """
    check_not_empty(values)
    return sum(values) / len(values)


def get_median(values):
    """Compute the median of a list of numbers without modifying it.

    Parameters
    ----------
    values : list of int or float
        Non-empty list of numbers.

    Returns
    -------
    float
        Middle value of the sorted list, or the mean of the two middle
        values when the list has an even length.

    Raises
    ------
    ValueError
        If values is empty.
    """
    check_not_empty(values)
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return float(ordered[middle])
    return (ordered[middle - 1] + ordered[middle]) / 2


def get_std(values):
    """Compute the population standard deviation of a list of numbers.

    Parameters
    ----------
    values : list of int or float
        Non-empty list of numbers.

    Returns
    -------
    float
        Square root of the mean squared distance from the mean.

    Raises
    ------
    ValueError
        If values is empty.
    """
    mean = get_mean(values)
    squared_diffs = [(value - mean) ** 2 for value in values]
    return math.sqrt(sum(squared_diffs) / len(values))
