from pg4nosql.PostgresNoSQLClient import PostgresNoSQLClient


def main():
    # create pg4nosql client
    pg4nosql = PostgresNoSQLClient(host='localhost')

    # create demo database
    demo_db = pg4nosql['demo']

    # create document only table
    users = demo_db['users']

    # create document & relational table
    cities = demo_db.get_or_create_table('cities', size='real')

    # None String Test
    cities.put({'name': 'Test'}, size=None)

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

    # commit data
    demo_db.commit()

    # query all users which are 24 years old
    users_24 = users.query("json->>'age'='24'")

    # query all cities which start with be and are bigger than 100 km
    big_ber_cities = cities.query("json->>'name' LIKE 'Ber%'"
                                  "AND size > 100")

    print map(lambda u: str(u), users_24)
    print map(lambda u: str(u), big_ber_cities)

    # get first city of the result array
    first_city = big_ber_cities[0]

    # read JSON attribute
    city_name = first_city.json['name']

    # change florian's age
    florian = users_24[0]
    florian.json['age'] = 25

    users.save(florian)
    users.commit()

    # make zurich a bit bigger
    zurich = cities.query_one("json->>'name'='Zurich'")
    zurich['size'] = 90

    cities.save(zurich)
    cities.commit()

    # close db
    demo_db.close()


if __name__ == '__main__':
    main()
