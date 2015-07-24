from pg4nosql.PostgresNoSQLClient import PostgresNoSQLClient


def main():
    # create pg4nosql client
    pg4nosql = PostgresNoSQLClient(host='localhost')

    # create demo database
    demo_db = pg4nosql.get_or_create_database('demo')

    # create document only table
    users = demo_db.get_or_create('users')

    # create document and relational table
    cities = demo_db.get_or_create('cities', {'size': 'real'})

    # store data into users
    users.put({'name': 'Florian', 'age': 24})
    users.put({'name': 'Markus', 'age': 24})
    users.put({'name': 'Sara', 'age': 22})
    users.put({'name': 'Thomas', 'age': 25})

    # store data into cities
    cities.put({'name': 'Zurich'}, relational_data={'size': '87.88'})
    cities.put({'name': 'Berlin'}, relational_data={'size': '891.8'})
    cities.put({'name': 'Bern'}, relational_data={'size': '51.6'})
    cities.put({'name': 'London'}, relational_data={'size': '1572'})

    # commit data
    demo_db.commit()

    # query all users which are 24 years old
    users_24 = users.query("data->>'age'='24'")

    # query all cities which start with be and are bigger than 100 km
    big_ber_cities = cities.query("data->>'name' LIKE 'Ber%'"
                                  "AND size > 100")

    print map(lambda u: str(u.relational), users_24)
    print map(lambda u: str(u.relational), big_ber_cities)

    # change florian's age
    florian = users_24[0]
    florian['age'] = 25

    users.save(florian)
    users.commit()

    # make zurich a bit bigger
    zurich = cities.query_one("data->>'name'='Zurich'")
    zurich.relational['size'] = 90

    cities.save(zurich)
    cities.commit()

    # close db
    demo_db.close()

if __name__ == '__main__':
    main()
