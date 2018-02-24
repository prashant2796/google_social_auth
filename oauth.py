"""
Following is a python script for Oauth2 implementation of google.
The same flow is applicable for any other oauth provider.

Firstly, the user is redirected to authorization link
which is google's sign in page where the user can sign in
with his google account and then grant permission 
to your app to access their data.

Then,the user is redirected back to redirected_url
with a authorization code appended in it.

This auth code is then send with a post request 
to authorization server to get back an access token.

The access token then can be send to resource server
to get back the user information.

"""



from flask import Flask, request

import requests

import datetime

import logging

import pytz

from pytz import timezone

from config import (CLIENT_ID,
					CLIENT_SECRET,
					AUTHORIZE_URL,
					CALLBACK_URL,
					ACCESS_TOKEN_URL,
					API_RESOURCE_URL,
					SCOPE_URL)

logging.basicConfig(filename='oauth.log',level=logging.ERROR)

app = Flask(__name__)
@app.route('/')

def homepage():
	"""
	Displays the authorization link to users.

	"""
	text = '<a href="%s">Login with google</a>'
	return text % get_authorization_url()


def get_authorization_url():

	"""
	This function returns the authorization url by appending 
	following parameters to it.
	
	authentication_parameters= {
								  "client_id":Your_client_id,
								  "redirect_uri":www.yourwebsite.com/oauth2callback,
								  "scope":"email",	
			  					  "response_type":"code",
								  "access_type":'offline',
								}


	When a user click on this link,the person is redirected 
	google sign in page where the user can login from his google
	credentials and can authorize the app.

	"""

	auth_parameters= {
					  "client_id":CLIENT_ID,
					  "redirect_uri":CALLBACK_URL,
					  "scope":SCOPE_URL,	
  					  "response_type":"code",
					  "access_type":'offline',
					 }

	# Makes a get request to authorization url with the parameter\
	# mentioned in the auth_parameters dictionary.				 
	auth_url =  requests.get(AUTHORIZE_URL,params=auth_parameters)
	

	return auth_url.url  # the .url method returns the url with parameters appended to it.

# This line indicates that when /oauth2callback url is encountered 
# which is our redirect url, the control is switched on to the following function.
@app.route('/oauth2callback') 


def google_call_back():
	"""
	The control is switched to this function when user is redirected
    after authorizing the client app.

	It returns the final user data which is defined in scope parameter.

	"""                                                           

	error = request.args.get('error', '')  # It gets the error specified in the url if any.
	if error:
		logging.error('Error occurred ' + error)  # Logging the error using log file

		# Returns back the user to homepage with printing error:access_denied
		return "Error: Access_denied   %s" %homepage() 

	# It gets the authorization code from the url 
	auth_code = request.args.get('code') 	

	# Takes in access token returned my the function	
	access_token = get_access_token(auth_code) 
	return "your google info is:%s" % get_user_info(access_token)                   


def get_access_token(auth_code):
	"""
	This function makes a post request which exchanges authorization code 
	for access token and returns it.
	
	access_token_parameters={
								"client_id":Your_client_id,
								"client_secret":your_client_secret,
								"redirect_uri":wwww.yourwebsite.com/oauth2callback,
								"code":code,  
								"grant_type":"authorization_code"
							}

	"""
	access_token_parameters={
								"client_id":CLIENT_ID,
								"client_secret":CLIENT_SECRET,
								"redirect_uri":CALLBACK_URL,
								"code":auth_code,
								"grant_type":"authorization_code"
							}

	# Sending a post request to get back the access token
	token_result = requests.post(ACCESS_TOKEN_URL,params=access_token_parameters) 

	access_token_result = token_result.json()  # Stores the json form of the result 
	return access_token_result["access_token"]  # Returns only the access token


def get_user_info(access_token):
	"""
	This function makes api calls to google resource server

	It exchanges access token to get user_info

	"""
	fmt = '%Y-%b-%d %H:%M:%S %Z%z' 
	timezone = pytz.timezone('Asia/Calcutta')

	# Localizes the current datetime with timezone of Asia/Calcutta
	local_dt = timezone.localize(datetime.datetime.now())  
	timezone_india = local_dt.strftime(fmt)
	Time_stamp = {
					"Timestamp":timezone_india
	             }

	resource_parameters= {

						"access_token":access_token,
						"Content-Type":"application/json"

					     }

	# Sending get request to resource server to get back the user informaton.
	user_info = requests.get(API_RESOURCE_URL, params=resource_parameters) 
	my_user_info = user_info.json() 

	# Using update method to add timestamp to json respone from google.
	my_user_info.update(Time_stamp)  
	return (my_user_info) 	         # Returns the user info in json provided by google



if __name__ == '__main__':
    app.run(debug=True)

