import sqlite3
import os
import re

def initdb():
    val = os.environ.get("PYSPELL_DB")
    if val is None:
        raise Exception("fail to init database. No environment variable PYSPELL_DB provided")
    return sqlite3.connect(val)

def ids_to_sql(name, *ids):
    _ids = []
    for id in ids:
        id = id.strip()
        if id == "":
            continue
        _id = id.split("-")
        if len(_id) == 1:
            _ids.append(f"{name} = {_id[0]}")
        elif len(_id) == 2:
            _ids.append(f"{name} >= {_id[0]} AND {name} <= {_id[1]}")
    
    return " AND ".join(_ids)
            

def get_schema(con, cur, table_name):
    cur.execute(f"select sql from sqlite_schema where name = '{table_name}'")
    con.commit()
    columns = None
    ll = cur.fetchall()
    while True:
        if len(ll) <= 0:
            break
        if len(ll[0]) <= 0:
            break

        match = re.match("[A-Za-z ]+\((.*)\)", ll[0][0].replace("\n", "").replace("\t", ""))
        if match is None:
            break
        
        s = match.group(1).strip()
        columns = [_.strip().split(" ")[0]  for _ in s.split(",")]
        break
    return columns