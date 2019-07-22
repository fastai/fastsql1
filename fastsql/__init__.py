import sqlalchemy, pandas as pd
from sqlalchemy import create_engine,MetaData,Table,Column,engine,sql
from sqlalchemy.sql.base import ImmutableColumnCollection

__all__ = 'pd conn_db patch'.split()

def conn_db(drivername, username=None, password=None, host=None, port=None, database=None):
    "Connect to DB using `url.URL()` params and return filled `MetaData`"
    eng= create_engine(engine.url.URL(drivername, username, password, host, port, database=database))
    eng.connect()
    meta = MetaData(bind=eng)
    meta.reflect()
    return meta

def patch(f):
    "Decorator to patch `f` into class of f's first param type annotation"
    cls = next(iter(f.__annotations__.values()))
    old_f = getattr(cls, f.__name__, None)
    def _f(o, *a, **k): return f(o, old_f, *a, **k) if old_f else f(o, *a, **k)
    setattr(cls,f.__name__,_f)
    return f

@patch
def __getattr__(self:MetaData, n):
    if n in self.tables: return self.tables[n],self.tables[n].c
    raise AttributeError

@patch
def __dir__(self:ImmutableColumnCollection, old_f): return old_f(self) + self.keys()
@patch
def __dir__(self:MetaData,                  old_f): return old_f(self) + list(self.tables)

@patch
def sql(self:engine.Engine, statement, *args, **kwargs):
    "Execute `statement` string and return `DataFrame` of results (if any)"
    t = self.execute(statement, *args, **kwargs)
    if not t.cursor: return
    return pd.DataFrame(t.fetchall(), columns=t.keys())

@patch
def sql(self:MetaData, statement, *args, **kwargs):
    "Execute `statement` string and return `DataFrame` of results (if any)"
    return self.bind.sql(statement, *args, **kwargs)

@patch
def df(self:engine.Engine, cmd):
    "Execute SqlAlchemy `cmd` and return `DataFrame` of results"
    return pd.read_sql(cmd, self)

@patch
def df(self:MetaData, cmd):
    "Execute SqlAlchemy `cmd` and return `DataFrame` of results"
    return self.bind.df(cmd)

@patch
def df(self:Table, where=None, limit=None):
    "`DataFrame` of table, optitionally limited by `where` and `limit` clauses"
    return self.bind.df(self.select(where).limit(limit))

