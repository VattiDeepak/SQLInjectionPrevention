import psycopg2

connection = psycopg2.connect(
    host="localhost",
    database="projecttest",
    user="postgres",
    password="heybuddyforthisworld",
    port=5432
)

def is_admin(username: str) -> bool:
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                admin
            FROM
                users
            WHERE
                username = '%s'
        """ % username)
        result = cursor.fetchone()

    if result is None:
        # User does not exist
        return False

    admin, = result
    return admin

print(is_admin("'; select true; --"))

connection.close()

#payload="'; select true; --"