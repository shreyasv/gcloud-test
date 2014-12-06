from bottle import route, run, template, request, redirect, static_file
import os

@route('/')
def index():
	print "Hello, World!!!"
	print foo
	return

port = int(os.environ.get("PORT",8081))
print 'PORT %d' % (port)
foo = os.environ.get("FOO", "Could Not Find FOO")
run(host='0.0.0.0', port=port)
