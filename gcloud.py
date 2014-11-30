from bottle import route, run, template, request, redirect, static_file

@route('/')
def index():
	return "Hello, World!!!"


run(host='localhost', port=8081)
