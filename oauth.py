"""
Following is a python script for Oauth2 implementation of google.The same flow is applicable for any other oauth provider.

Firstly, the user is redirected to authorization link which is google's sign in page where the user can sign in with his google account and then grant permission to your app to access their data.

Then, the user is redirected back to redirected_url  with a authorization code appended in it.

This auth code is then send with a post request to authorization server to get back an access token.

The access token then can be send to resource server to get back the user information.

"""


from config import (CLIENT_ID,
					CLIENT_SECRET,
					AUTHORIZE_URL,
					CALLBACK_URL,
					ACCESS_TOKEN_URL,
					API_RESOURCE_URL,
					SCOPE_URL)
from flask import Flask, abort, request
import requests
import datetime

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
	this function returns the authorization url

	it makes a get request to the authorization 
	url of google and  with the parameters
	that are appended to it.

	when a user click on this link,the person is redirected 
	google sign in page where the user can login from his google
	credentials and can authorize the app.

	"""

	auth_parameters= {"client_id":CLIENT_ID,
					  "redirect_uri":CALLBACK_URL,
					  "scope":SCOPE_URL,	
  					  "response_type":"code",
					  "access_type":'offline',
   					  "include_granted_scopes":'true'				  
					 }
	auth_url=requests.get(AUTHORIZE_URL,params=auth_parameters) 
	#makes a get request to authorization url with the parameters mentioned in the auth_parameters dictionary.

	return auth_url.url   #the .url method returns the url with parameters appended to it.

@app.route('/oauth2callback') #this line indicates that when /oauth2callback url is encountered which is our redirect url,the control is switched on to this function.
def google_call_back():
	"""
	The control is switched to this function when user is redirected after authorizing the client app.

	It returns the final user data which is defined in scope parameter.

	"""
	error = request.args.get('error', '')   #gets the error specified in the url if any.  
	if error:
	    return "Error: " + error        #returns the error if there is one.

	auth_code = request.args.get('code')  #it gets the authorization code from the url 
	access_token = get_access_token(auth_code) #takes in access token returned my the function
	return "your google info is:%s" % get_user_info(access_token)

def get_access_token(auth_code):
	"""
	this function makes a post request which exchanges authorization code for 
	access token and returns it.
	
	to get the access token you can either make a get or post request to access 
	token url.
	but in case of google, it allows only post request.

	"""
	access_token_parameters={
								"client_id":CLIENT_ID,
								"client_secret":CLIENT_SECRET,
								"redirect_uri":CALLBACK_URL,
								"code":auth_code,
								"grant_type":"authorization_code"
							}

	
	token_result=requests.post(ACCESS_TOKEN_URL,params=access_token_parameters) # a post request to get back the access token
	access_token_result = token_result.json()    #stores the json form of the result 
	return access_token_result["access_token"]   #returns only the access token


def get_user_info(access_token):
	"""
	this function makes api calls to google resource server

	it exchanges access token to get user_info

	"""
	# Timestamp='Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())

	Time_stamp = {
					"Timestamp":'{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())
	}
	resource_parameters={

						"access_token":access_token,
						"Content-Type":"application/json"

					}

	user_info=requests.get(API_RESOURCE_URL, params=resource_parameters) #get request to resource server to get back the user informaton
	my_user_info=user_info.json() 
	my_user_info.update(Time_stamp)  #using update method to add timestamp to json 
	return (my_user_info) 	                 #returns the user info in json provided by google

# def get_time_stamp():
# 	Timestamp='Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())
# 	return Timestamp



if __name__ == '__main__':
    app.run(debug=True)
