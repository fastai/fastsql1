import sqlalchemy, pandas as pd
from sqlalchemy import create_engine,MetaData,Table,Column
from sqlalchemy.engine import url
from sqlalchemy.sql.base import ImmutableColumnCollection

__all__ = 'pd conn_db patch'.split()

def conn_db(drivername, username=None, password=None, host=None, port=None, database=None):
    engine = create_engine(url.URL(drivername, username, password, host, port, database=database))
    engine.connect()
    meta = MetaData(bind=engine)
    meta.reflect()
    return meta

def patch(f):
    n = f.__name__
    cls = next(iter(f.__annotations__.values()))
    old_f = getattr(cls, n, None)
    def _inner(self, *args, **kwargs):
        return f(self, old_f, *args, **kwargs) if old_f else f(self, *args, **kwargs)
    setattr(cls,n,_inner)
    return f

@patch
def __dir__(self:ImmutableColumnCollection, old_f): return old_f(self) + self.keys()
@patch
def __dir__(self:MetaData,                  old_f): return old_f(self) + list(self.tables)

@patch
def __getattr__(self:MetaData, n):
    if n is None: raise AttributeError
    res = Table(n, self, autoload=True)
    return res,res.c

@patch
def df(self:Table, where=None, limit=None):
    return pd.read_sql(self.select(where).limit(limit), self.bind)

