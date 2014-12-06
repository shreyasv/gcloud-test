from bottle import route, run, template, request, redirect, static_file
import os
import psycopg2
import urlparse

@route('/')
def index():
	return foo * 2

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])
print url
conn = psycopg2.connect(
	database=url.path[1:],
	user=url.username,
	password=url.password,
	host=url.hostname,
	port=url.port
)

cursor = conn.cursor()
cursor.execute("select * from test")
val = cursor.fetchone()
print val

port = int(os.environ.get("PORT",8081))
print 'PORT... %d' % (port)
foo = os.environ.get("FOO", "Could Not Find FOO")
run(host='0.0.0.0', port=port)
