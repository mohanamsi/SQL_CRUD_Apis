
class BuildQuery(object):
    # post query

    def build_query(self, query_params):
        query = "select * from users where "
        # print(f"query_params = {query_params}")

        # del query_params['operator']
        print(f"query_params = {query_params}")
        if len(query_params) != 1:
            operator = query_params['operator']
            for i, j in enumerate(query_params.items()):
                print(i, j)
                if j[0] == "operator":
                    print(j[0])
                    continue
                if isinstance(j[1], str):
                    ext_query = f"{j[0]}='{j[1]}'"
                    query = query + ext_query
                    if i < len(query_params) - 2:
                        query = query + f" {operator} "
                elif isinstance(j[1], list):
                    if len(j[1]) < 2:
                        ext_query = f"{j[0]}='{j[1][0]}'"
                    else:
                        ext_query = f"{j[0]} in {tuple(j[1])}"
                    query = query + ext_query
                    if i < len(query_params) - 2:
                        query = query + f" {operator} "
            return query
        else:
            for i, j in enumerate(query_params.items()):
                query = query + f"{j[0]} = '{j[1]}'"
            return query

    # update(patch) query
    def update_query(self, d):
        query = "UPDATE users set "
        print(f"d = {d}")
        """ UPDATE employe set Name=%s, Salary = %s where id=%s and  """
        leng_set = len(d['new'])
        for i, j in enumerate(d['new'].items()):
            print(i, j)
            query = query + f"{j[0]} = '{j[1]}'"
            if i < leng_set - 1:
                query = query + ','

        query = f"{query}  where "
        # print(query)
        d.pop('new')
        if len(d) > 1:
            operator = d['operator']
            d.pop('operator')
            for i, j in enumerate(d.items()):
                print(i, j)
                ext = f"{j[0]} = '{j[1]}'"
                query = query + ext
                if i < len(d) - 1:
                    query = query + f" {operator} "
            return query
        else:
            for i, j in enumerate(d.items()):
                ext = f"{j[0]} = '{j[1]}'"
                query = query + f" {ext} "
        return query

    # insert(put) query
    def insert_query(self, data):
        query = "INSERT INTO users "
        columns = []
        for i in data:
            columns.append(i)
        columns = tuple(columns)
        k = ','.join(columns)
        # query = f"{query} ({k})"
        query = query + '(' + k + ')'
        value = []
        for i in data.values():
            value.append(i)
        value = tuple(value)
        print(value)
        query = query + ' values' + str(value)
        return query

    # delete query
    def delete_query(self, params):
        print('delete')
        query = "DELETE FROM users WHERE "

        params = params
        print(f"{params}")
        if len(params) > 1:
            operator = params['operator']
            print(operator)
            for i, j in enumerate(params.items()):
                print(i, j)
                if j[0] == "operator":
                    print(j[0])
                    continue
                if isinstance(j[1], str):
                    ext_query = f"{j[0]}='{j[1]}'"
                    query = query + " " + ext_query
                    if i < len(params) - 2:
                        query = query + f" {operator} "
                elif isinstance(j[1], list):
                    if len(j[1]) < 2:
                        ext_query = f"{j[0]}='{j[1][0]}'"
                    else:
                        ext_query = f"{j[0]} in {tuple(j[1])}"
                    query = query + ext_query
                    if i < len(params) - 2:
                        query = query + f" {operator} "
        else:
            for i, j in enumerate(params.items()):
                print(i, j)
                if isinstance(j[1], str):
                    ext_query = f"{j[0]}='{j[1]}'"
                    query = query + " " + ext_query
                elif isinstance(j[1], list):
                    if len(j[1]) < 2:
                        ext_query = f"{j[0]}='{j[1][0]}'"
                    else:
                        ext_query = f"{j[0]} in {tuple(j[1])}"
                    query = query + ext_query

        return query
