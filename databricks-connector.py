import redis
from saver import MySQLManager


r = redis.Redis(host='localhost',
                port=6379,
                db=0)
r.set('foo', 'bar')

saver = MySQLManager(host="localhost",
                      port=3306,
                      user="root",
                      password="Pr0tett0.98",
                      database="project_bdt")


def sql_to_redis(saver: MySQLManager, table_name: str):
    r_redis = r
    print("")
    print("Connected to Redis successfully!")

    cursor = saver.connection.cursor()
    select = 'SELECT * FROM {} LIMIT 100'.format(table_name)
    # select = 'SELECT * FROM records WHERE location_id = 9'
    cursor.execute(select)
    data = cursor.fetchall()

    # Clean redis before run again
    # This is for test purpose
    r_redis.delete("all_records")

    # Put all data from MySQL to Redis
    for row in data:
        r_redis.rpush("all_records", row[3])

    # Close connection to DB and Cursor
    cursor.close()
    print("done")


sql_to_redis(saver, "final")


