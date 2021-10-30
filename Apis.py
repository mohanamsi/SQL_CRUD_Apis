from sanic import Sanic
import io
from sanic import HTTPResponse
import json
import mysql.connector
from BuildQuery import BuildQuery

app = Sanic("My First Sanic App")


connection = mysql.connector.connect(host='localhost', user='root', password='999M@mmu999', database='Electronics')
cursor = connection.cursor()

# webapp path defined used route decorator
obj = BuildQuery()

# def build_query(query_params):
#     query = "select * from users where "
#     # print(f"query_params = {query_params}")
#
#     # del query_params['operator']
#     print(f"query_params = {query_params}")
#     if len(query_params) != 1:
#         operator = query_params['operator']
#         for i, j in enumerate(query_params.items()):
#             print(i, j)
#             if j[0] == "operator":
#                 print(j[0])
#                 continue
#             if isinstance(j[1], str):
#                 ext_query = f"{j[0]}='{j[1]}'"
#                 query = query + ext_query
#                 if i < len(query_params) - 2:
#                     query = query + f" {operator} "
#             elif isinstance(j[1], list):
#                 if len(j[1]) < 2:
#                     ext_query = f"{j[0]}='{j[1][0]}'"
#                 else:
#                     ext_query = f"{j[0]} in {tuple(j[1])}"
#                 query = query + ext_query
#                 if i < len(query_params) - 2:
#                     query = query + f" {operator} "
#         return query
#     else:
#         for i, j in enumerate(query_params.items()):
#             query = query + f"{j[0]} = '{j[1]}'"
#         return query


@app.route("/fetch_data", methods=['POST'])
def fetch_data(request):
    data = io.BytesIO(request.body)
    data = json.load(data)
    query = obj.build_query(data)
    print(query)
    cursor.execute(query)
    records = cursor.fetchall()
    records = [dict(zip(cursor.column_names, i)) for i in records]
    print(records)
    return HTTPResponse(json.dumps(records))

# def insert_query(data):
#     query = "INSERT INTO users "
#     columns = []
#     for i in data:
#         columns.append(i)
#     columns = tuple(columns)
#     k = ','.join(columns)
#     # query = f"{query} ({k})"
#     query = query + '('+k+')'
#     value = []
#     for i in data.values():
#         value.append(i)
#     value = tuple(value)
#     print(value)
#     query = query+' values' + str(value)
#     return query


@app.route("/insert_data", methods=['PUT'])
def put(request):
    # cursor = self.connection.cursor()
    # query = """ INSERT INTO Laptop (Id,Name,Price,Purchase_date)
    #             VALUES(%s,%s,%s,%s)"""
    # cursor.execute(query, ('20', 'Vivo', '6459', '2019-12-16'))
    # connection.commit()
    record = io.BytesIO(request.body)
    record = json.load(record)
    print(record)
    query = obj.insert_query(record)
    print(f"SqlQuery = {query}")
    cursor.execute(query)
    connection.commit()
    return HTTPResponse(json.dumps(record))

# def update_query(d):
#     query = "UPDATE users set "
#     print(f"d = {d}")
#     """ UPDATE employe set Name=%s, Salary = %s where id=%s and  """
#     leng_set = len(d['new'])
#     for i, j in enumerate(d['new'].items()):
#         print(i, j)
#         query = query + f"{j[0]} = '{j[1]}'"
#         if i < leng_set - 1:
#             query = query + ','
#
#     query = f"{query}  where "
#     # print(query)
#     d.pop('new')
#     if (len(d) != 1):
#         operator = d['operator']
#         d.pop('operator')
#         for i, j in enumerate(d.items()):
#             print(i, j)
#             ext = f"{j[0]} = '{j[1]}'"
#             query = query + ext
#             if i < len(d) - 1:
#                 query = query + f" {operator} "
#         return (query)
#     else:
#         ext = f"{j[0]} = '{j[1]}'"
#         query = query + f" {ext} "
#     return (query)


@app.route("/update_data", methods=['PATCH'])
def patch(request):
    detail = io.BytesIO(request.body)
    detail = json.load(detail)
    print(f"detail={detail}")
    query = obj.update_query(detail)
    print(f"SqlQuery={query}")
    cursor.execute(query)
    connection.commit()
    return HTTPResponse(json.dumps(detail))

# def delete_query(params):
#     print('delete')
#     query = "DELETE FROM users WHERE "
#
#     params = params
#     print(f"{params}")
#     if len(params) >1:
#         operator = params['operator']
#         print(operator)
#         for i, j in enumerate(params.items()):
#             print(i, j)
#             if j[0] == "operator":
#                 print(j[0])
#                 continue
#             if isinstance(j[1], str):
#                 ext_query = f"{j[0]}='{j[1]}'"
#                 query = query + " " + ext_query
#                 if i < len(params) - 2:
#                     query = query + f" {operator} "
#             elif isinstance(j[1], list):
#                 if len(j[1]) < 2:
#                     ext_query = f"{j[0]}='{j[1][0]}'"
#                 else:
#                     ext_query = f"{j[0]} in {tuple(j[1])}"
#                 query = query + ext_query
#                 if i < len(params) - 2:
#                     query = query + f" {operator} "
#     else:
#         for i, j in enumerate(params.items()):
#             print(i, j)
#             if isinstance(j[1], str):
#                 ext_query = f"{j[0]}='{j[1]}'"
#                 query = query + " " + ext_query
#             elif isinstance(j[1], list):
#                 if len(j[1]) < 2:
#                     ext_query = f"{j[0]}='{j[1][0]}'"
#                 else:
#                     ext_query = f"{j[0]} in {tuple(j[1])}"
#                 query = query + ext_query
#
#     return query


@app.route("/delete_data", methods=['DELETE'])
def delete(request):
    # record = io.BytesIO(request.body)
    # record = json.load(record)
    # print(record)
    data = io.BytesIO(request.body)
    data = json.load(data)
    print(data)

    query = obj.delete_query(data)
    print(query)
    cursor.execute(query)
    return HTTPResponse(json.dumps(data))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
