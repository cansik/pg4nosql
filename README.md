# pg4nosql

[![Build Status](https://travis-ci.org/cansik/pg4nosql.svg)](https://travis-ci.org/cansik/pg4nosql)
[![Code Climate](https://codeclimate.com/github/cansik/pg4nosql/badges/gpa.svg)](https://codeclimate.com/github/cansik/pg4nosql)
[![Latest Version](https://img.shields.io/pypi/v/pg4nosql.svg)](https://pypi.python.org/pypi/pg4nosql)
[![Development Status](https://img.shields.io/pypi/status/pg4nosql.svg)](https://pypi.python.org/pypi/pg4nosql)
[![Python Versions](https://img.shields.io/pypi/pyversions/pg4nosql.svg)](https://pypi.python.org/pypi/pg4nosql)
[![License](https://img.shields.io/pypi/l/pg4nosql.svg)](https://github.com/cansik/pg4nosql/blob/master/LICENSE.txt)

A simple psycopg2 based wrapper for nosql like database interaction with python.

### Why another wrapper?
The wrapper was developed to work with JSON postgres storage like a real NoSQL DB (e.g. MongoDB). After a long research with google there was no library found which helps to work with JSON and PostgreSQL so I decided to develop one.

The strength of the wrapper is that you still can have multiple relational colums in your table.

### Installation

##### Using [Python Package Index](https://pypi.python.org/pypi/pg4nosql) (PIP)
Just run the command:
`pip install pg4nosql`

*During alpha stage the api will change with each build. So try to stay with one version if you want to use it.*

##### The hacky way
1. [download](https://github.com/cansik/pg4nosql/tarball/0.4.2) or clone this repository
2. run the command `python setup.py install`

### Changelog
* Version `0.4.2`
  * fixed python 3.3 iterator return
* Version `0.4.1`
  * Query from view
  * fixed some bugs
* Version `0.4.0`
  * adds join query statements
  * adds update method
  * adds save method on result item
* Version `0.3.7`
  * adds the support for non-json database tables
* Version `0.3.6`
  * id datatype can be set on table creation
* Version `0.3.3`
  * project cleanup
* Version `0.3.1`
  * auto-commit for very operation as default
  * save does not affect saving object anymore
  * bug fixes
* Version `0.2.4`
  * a lot of bug fixes
* Version `0.2.0`
  * added port argument
  * replaced dictionary argument with **keyword syntax
  * switched result.relational with result.json
  * add bracket syntax to get database or table
  * renamed table.get\_or\_create to match codestyle

### Example
These examples show the funcionality of the wrapper. There are some functions which are not covered by the examples (like removing of a table) but the importent ones are explained.

##### Dataschema Creation
To create the dataschema you can use normal database tools if you want. A document table has two fields:

* `id` with data type **serial**
* `json` with data type **JSON** which represents the document

But pg4nosql also provides methods to create your database schema on the fly. This is useful to create tables and databases software controlled.

This example shows how to create a database and their tables. The cities table is special because it also contains relational data like a normal table would:

```python
# create pg4nosql client
pg4nosql = PostgresNoSQLClient(host='localhost')

# create demo database
demo_db = pg4nosql['demo']

# create document only table
users = demo_db['users']

# create document & relational table
cities = demo_db.get_or_create_table('cities', size='real NOT NULL')
```

###### Row Identifier Type
By default the `id` row type is `SERIAL` but in some cases it is necessary to define the type yourself. This is possible with the `row_identifier_type` argument.

```python
# create document table with bigserial
big_users = demo_db.create_table('big_users',
								  row_identifier_type='BIGSERIAL')
```

##### Insert Data
To insert data into the table you just hand over a dictionary or an object which is json serializable. If there are relational columns defined you can set those by the table name as keyword and the value:

```python
# store data into users table
users.put({'name': 'Florian', 'age': 24})
users.put({'name': 'Markus', 'age': 24})
users.put({'name': 'Sara', 'age': 22})
users.put({'name': 'Thomas', 'age': 25})

# store data into cities table
cities.put({'name': 'Zurich'}, size=87.88)
cities.put({'name': 'Berlin'}, size=891.8)
cities.put({'name': 'Bern'}, size=51.6)
cities.put({'name': 'London'}, size=1572)
```

If you work **without json documents**, there is just a normal `insert` method to store new records into a table.

```python
# store data into cities table
users.insert(age=25, name="Florian")
```

###### Lazy Commit
If you want to store or save multiple entries you can set the `auto_commit` argument to `False` and commit it yourself.

```python
# store data with lazy commit
for i in range(0, 255):
    users.put({'name': 'Test', 'age': i}, auto_commit=False)

# lazy commit data
users.commit()
```

##### Query Data
To get your data back you can run a query over it. This works like normal SQL WHERE queries. For **JSON** data you have to use the `json` column:

```python
# query all users which are 24 years old
users_24 = users.query("json->>'age'='24'")
```
And here the result of the user query:

```json
[  
   "{'json': {u'age': 24, u'name': u'Florian'}, 'id': 1}",
   "{'json': {u'age': 24, u'name': u'Markus'}, 'id': 2}"
]
```
You can also combine relational and JSON queries together like this:

```python
# query all cities which start with be and are bigger than 100 km
big_ber_cities = cities.query("json->>'name' LIKE 'Ber%'"
                              "AND size > 100")
```
Here the result of this query:

```json
[  
   "{'json': {u'name': u'Berlin'}, 'id': 2, 'size': 891.8}"
]
```

##### Query with Join
It is also possible to create simple *joined* queries with the function `query_join`. Consider a datamodel with an `user` table and an `address` table. This two tables are connected through a *foreign key* `fk_user`.

The called table get's the identifier `a` and the joined table the identifier `b`.

```python
# get all users with their address
users = user.query_join('address', 'a.id = b.fk_user')
```

##### Query from View
To query data from a view you have to get the view from the database and then it has the same query method like a table.

```python
# get view
self.user_view = self.database.get_view('user_view')

# query data
records = self.user_view.query()
```

##### Query Data Access
To **access** the **JSON** fields of the result there is an attribute called `json`:

```python
# get first city of the result array
first_city = big_ber_cities[0]

# read JSON attribute
city_name = first_city.json['name']
```
To **access** the **relational** fields of the result you have to use **square brackets** (`[]`) on the result:

```python
# read relational attribute
city_size = first_city['size']
```
There is also a default field called `id` which contains the default row identifier for easy access:

```python
# get id of row
city_id = first_city.id
```

##### Update Data
With those access methods you can also write into the result and change the values of the fields. To save it just call `save(obj)` on the table object.

```python
# change florian's age
florian = users_24[0]
florian.json['age'] = 25

users.save(florian)
```
The same works also with the `relational` fields:

```python
# make zurich a bit bigger
zurich = cities.query_one("data->>'name'='Zurich'")
zurich['size'] = 90

cities.save(zurich)
```

With the release `0.4.0` it is also possible to save the database object directly:
```python
# make zurich a bit bigger
zurich = cities.query_one("data->>'name'='Zurich'")
zurich['size'] = 90

zurich.save()
```


**Without json documents**, there is just a normal `update` method to update new records into a table.

```python
# store data into cities table
florian = users_24[0]
florian['name'] = 'Markus'
users.update(florian)
```

##### Direct Execution
It is also possible to directly execute sql statements as you are used to. The execute function is declared on the database object and on the table object.

```python
# run simple sql query
my_data = demo_db.execute('SELECT * FROM cities')
```

##### Close Connection
Finally don't forget to close the connection to the database.

```python
# close db
demo_db.close()
```

### About
The wrapper has been written for a science project and is still an early beta version!
Idea and implementation by Florian (cansik)

MIT License
Copyright (c) 2015
