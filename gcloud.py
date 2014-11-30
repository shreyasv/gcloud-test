from bottle import route, run, template, request, redirect, static_file
import admin
import db
import home
import httplib2
import StringIO
import urlparse
import sys
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
import os
import parse

@route('/')
def index():
	return home.renderLogin()

@route('/login', method='POST')
def login():
	email = request.forms.get('email')
	userid = db.getUserId(email)
	if not userid:
		(name, domain) = email.split('@')
		db.createUser(name, email)
		userid = db.getUserId(email)
	redirect('/'+str(userid)+'/home')

@route('/<userid>/home')
def index(userid):
	userid = int(userid)
	return home.render(userid)

@route('/<userid>/send-message', method='POST')
def send_message(userid):
	userid = int(userid)
	
	#Try to get a selected contact from the radio buttons first...
	toEmail = request.forms.get('friend')
	
	if not toEmail:
		#Otherwise see if there's a new address in the To: box
		toEmail = request.forms.get('toEmail')
	message = request.forms.get('message')
	if not message or message.strip == "":
		return "Please type a real message!"
	toUserId = db.getUserId(toEmail)
	if not toUserId:
	
		#This is just for testing purposes, allow a user to create a contact by emailing a new email address	
		(name,domain) = toEmail.split('@')
		db.createUser(name,toEmail)
		toUserId = db.getUserId(toEmail)
		db.createContact(userid,toUserId)

	status = db.newMessage(userid, toUserId, message)
	#return 'sent "' + message + '" to ' + toEmail + '<a href=/{userid}/home> Back to Inbox</a>'.format(userid=userid)
	redirect_uri = '/%d/home' % (userid)
	redirect(redirect_uri)

@route('/admin')
def admin_page():
	return admin.render()

@route('/admin-add-user', method='POST')
def admin_add_user():
	name = request.forms.get('name')
	email = request.forms.get('email')
	return admin.add_user(name, email)

@route('/admin-clear-db', method='POST')
def admin_clear_db():
	db.clearDb()
	redirect('/admin')


@route('/static/<filename>')
def server_static(filename):
	print "routing static file"
	return static_file(filename,root='/Users/shreyas/slowchat')

@route('/get-contacts')
def get_contacts():

	print "##" + request.url
	
	storage_path = 'credentials-.dat'

	authorize = request.query.authorize
	if authorize:
		print 'Checking if has credentials'
	
		#credentials = get_credentials(userid)
		storage = Storage(storage_path)
		credentials = storage.get()	

		if credentials is None or credentials.invalid:

			#set cookie so we know who it is
			#do this later			

			print "Beginning Flow Step 1"
			uri = flow.step1_get_authorize_url()
			print '***' + uri
			redirect(uri)
		else:
			print "ALREADY AUTHORIZED!!!!"
	
	code = request.query.code
	if code:
		print "## Entering Flow Phase 2 (have code)"		
		credentials = flow.step2_exchange(code)
		
		#save_credentials(userid, credentials)
		storage = Storage(storage_path)
		storage.put(credentials)		

				
	http = httplib2.Http()
	http = credentials.authorize(http)

	# don't need to make queries everytime, so will write one resultset out and reuse it

	if os.path.isfile('contacts.txt'):
		pass
	else:
		ret_tuple = http.request('https://www.google.com/m8/feeds/contacts/default/full')
		f = open('contacts.txt','w')
		f.write(ret_tuple[1])	
		f.close()
	
	#contacts.txt goes away once we figure out how to parse the feed output

	g = open('contacts.txt','r')
	contactsXML = g.read()
	g.close()
	parse.parseContacts(2,contactsXML)	
	
	# HACK SINCE IT ONLY WORKS FOR ME
	redirect_home = '/2/home'
	redirect(redirect_home)


client_id = ''
client_secret = ''

if os.path.isfile('config.txt'):

	config = open('config.txt','r')
	client_id = config.readline().rstrip('\n')
	client_secret = config.readline().rstrip('\n')
	config.close()
	
redir_uri = 'http://localhost:8080/get-contacts'
flow = OAuth2WebServerFlow(client_id, client_secret,'https://www.google.com/m8/feeds/',redirect_uri=redir_uri)

run(host='localhost', port=8080)
