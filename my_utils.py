def get_column(file_name, query_column, query_value, result_column):
    result = []
    with open(file_name, "r") as f:
        lines = f.readlines()

    if not lines:
        print(f"---\nWarning: {file_name} was empty. Returning an empty list...\n---")
        return result

    headers = lines[0].strip().split(",")
    query_col_idx = (
        query_column if isinstance(query_column, int) else headers.index(query_column)
    )
    result_col_idx = (
        result_column
        if isinstance(result_column, int)
        else headers.index(result_column)
    )

    for line in lines[1:]:
        values = line.strip().split(",")
        if values[query_col_idx] == query_value:
            result.append(values[result_col_idx])

    return result
