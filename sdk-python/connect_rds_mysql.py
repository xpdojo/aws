import sys

import pymysql

"""
ref: https://docs.aws.amazon.com/lambda/latest/dg/services-rds-tutorial.html
"""

# rds settings
RDS_HOST = "endpoint"
RDS_DATABASE = "database"
RDS_USERNAME = "username"
RDS_PASSWORD = "password"

# create the database connection outside of the handler to allow connections to be
# re-used by subsequent function invocations.
try:
    conn = pymysql.connect(
        host=RDS_HOST,
        db=RDS_DATABASE,
        user=RDS_USERNAME,
        passwd=RDS_PASSWORD,
        connect_timeout=5
    )
except pymysql.MySQLError as e:
    print("ERROR: Unexpected error: Could not connect to MySQL instance.")
    print(e)
    sys.exit()

print("SUCCESS: Connection to RDS MySQL instance succeeded")


def lambda_handler(event, context):
    """
    This function creates a new RDS database table and writes records to it
    """
    item_count = 0
    with conn.cursor() as cur:
        cur.execute("""
        select *
        from table_name
        """)
        print("The following items have been added to the database:")
        for row in cur:
            item_count += 1
            print(row)
    conn.commit()

    return "List %d items from RDS MySQL table" % item_count


if __name__ == "__main__":
    print(lambda_handler(None, None))
