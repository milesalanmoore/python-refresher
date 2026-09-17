"""Utilities for pulling numeric columns out of a CSV file.

* get_column - return the values of one column where another column matches
"""


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
