## fastsql

A bit of extra usability for sqlalchemy.

### Install

```bash
pip install git+https://github.com/jph00/fastsql
```

### Usage examples

Connect to db and return filled `MetaData` object (sqlalchemy format)
```
# from https://pypi.org/project/python-dotenv/
load_dotenv('.env.local')

USER = environ['SQLUSER']
PASS = environ['SQLPASS']
DRIV = 'mysql+pymysql'
DB   = 'prisma'
HOST = '127.0.0.1'
PORT = 3306

db = conn_db(DRIV, USER, PASS, HOST, PORT, DB)
```

Show list of table names
```
' '.join(db.tables)
```

Get the `User` table. Note that `db` supports tab completion of table names here. The `Table` object and collection of columns is returned as a tuple.
```
u,uc = db.User
```

The collection of columns supports tab completion too.
```
uc.billingAddress
```

Get a data frame, with optional `where` clause and `limit`, with the `df` method on either `Table` or `MetaData`.
```
# These are equivalent
u.df(where=uc.email.startswith('j'), limit=1)
db.df(u.select(uc.email.startswith('j'), limit=1))
```

You can also pass SQL statements directly.
```
# returns a DataFrame
db.sql("select count(*) from User")
# returns None
db.sql("insert into User select * from User where email = 'xxx'")
```

