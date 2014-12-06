from bottle import route, run, template, request, redirect, static_file
import os

@route('/')
def index():
	return "Hello, World!!!"

port = int(os.environ.get("PORT",8081))
print 'PORT!!!!!!! %d' % (port)
print os.environ.get("FOO", "Could Not Find FOO")
run(host='0.0.0.0', port=port)
