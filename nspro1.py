import psycopg2
from psycopg2 import sql

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
                username = %(username)s
        """, {
            'username': username
        })
        result = cursor.fetchone()

    if result is None:
        # User does not exist
        return False

    admin, = result
    return admin

def count_rows(table_name: str, limit: int) -> int:
    with connection.cursor() as cursor:
        stmt = sql.SQL("""
            SELECT
                COUNT(*)
            FROM (
                SELECT
                    1
                FROM
                    {table_name}
                LIMIT
                    {limit}
            ) AS limit_query
        """).format(
            table_name = sql.Identifier(table_name),
            limit = sql.Literal(limit),
        )
        cursor.execute(stmt)
        result = cursor.fetchone()

    rowcount, = result
    return rowcount

#print(is_admin("'; select true; --"))
print(count_rows("(select 1) as foo; update users set admin = true where name = 'haki'; --", 1))

connection.close()