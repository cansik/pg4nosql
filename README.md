# pg4nosql
A simple psycopg2 based wrapper for nosql like database interaction with python.

### Background
The wrapper was developed to work with JSON postgres storage like a real NoSQL DB (e.g. MongoDB). After a long research with google there was no library found which helps to work with JSON and PostgreSQL so I decided to develop one.

The strength of the wrapper is that you still can have multiple relational colums in your table.

### Installation
1. download or clone this repository (current release: `0.1.1`)
2. run the command `python setup.py install`

### Example
These examples show the funcionality of the wrapper. There are some functions which are not covered by the example (like removing of a table) but the importent is explained.

##### Dataschema Creation
To create the datashema you can use database tools if you want. A document table has two fields:

* `id` with data type **serial**
* `data` with data type **JSON** which represents the document

But pg4nosql also provides methods to create your database schema on the fly. This is useful to create tables and databases software controlled.

This example shows how to create a database and their tables. The cities table is special because it also contains relational data like a normal table would:

```python
# create pg4nosql client
pg4nosql = PostgresNoSQLClient(host='localhost')

# create demo database
demo_db = pg4nosql.get_or_create_database('demo')

# create document only table
users = demo_db.get_or_create('users')

# create document and relational table
cities = demo_db.get_or_create('cities', {'size': 'real'})
```

##### Insert Data
To insert data into the table you just hand over a dictionary or an object which is json serializable. If there are relational columns defined you can set those by the parameter `relational_data`:

```python
# store data into users table
users.put({'name': 'Florian', 'age': 24})
users.put({'name': 'Markus', 'age': 24})
users.put({'name': 'Sara', 'age': 22})
users.put({'name': 'Thomas', 'age': 25})

# store data into cities table
cities.put({'name': 'Zurich'}, relational_data={'size': '87.88'})
cities.put({'name': 'Berlin'}, relational_data={'size': '891.8'})
cities.put({'name': 'Bern'}, relational_data={'size': '51.6'})
cities.put({'name': 'London'}, relational_data={'size': '1572'})

# commit data
demo_db.commit()
```

##### Query Data
To get your data back you can run a query over it. This works like normal SQL WHERE queries. For **JSON** data you have to use the `data` column:

```python
# query all users which are 24 years old
users_24 = users.query("data->>'age'='24'")
```
And here the result of the user query:

```json
[  
   "{'data': {u'age': 24, u'name': u'Florian'}, 'id': 1}",
   "{'data': {u'age': 24, u'name': u'Markus'}, 'id': 2}"
]
```
You can also combine relational and JSON queries together like this:

```python
# query all cities which start with be and are bigger than 100 km
big_ber_cities = cities.query("data->>'name' LIKE 'Ber%'"
                              "AND size > 100")
```
Here the result of this query:

```json
[  
   "{'data': {u'name': u'Berlin'}, 'id': 2, 'size': 891.8}"
]
```

##### Query Data Access
To **access** the **JSON** fields of the result you have to use **square brackets** (`[]`) on the result.

```python
# get first city of the result array
first_city = big_ber_cities[0]

# read JSON attribute
city_name = first_city['name']
```
To **access** the **relational** fields of the result there is a attribute called `relational`:

```python
# read relational attribute
city_size = first_city.relational['size']
```

##### Update Data
With those access methods you can also write into the result and change the values of the fields. To save it just call `save(obj)` on the table object.

```python
# change florian's age
florian = users_24[0]
florian['age'] = 25

users.save(florian)
users.commit()
```
The same works also for the `relational` fields:

```python
# make zurich a bit bigger
zurich = cities.query_one("data->>'name'='Zurich'")
zurich.relational['size'] = 90

cities.save(zurich)
cities.commit()
```

##### Close Connection
Finally don't forget to close the connection to the database.

```python
# close db
demo_db.close()
```

### About
The wrapper has been written for a science project and is still an early alpha version!
Idea and implementation by Florian (cansik)