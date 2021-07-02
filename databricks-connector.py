import redis
import json
from saver import MySQLManager
from collections import defaultdict

r = redis.Redis(host='localhost',
                port=6379,
                db=0)
r.set('foo', 'bar')

saver = MySQLManager(host="localhost",
                      port=3306,
                      user="root",
                      password="Pr0tett0.98",
                      database="project_bdt")





