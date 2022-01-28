def dict_factory(cursor, row):
    d = {}
    print(f'cursor desc: {cursor.description}')
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
