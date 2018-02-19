CLIENT_ID='544125358258-jsnghl0v7lljccjpce93hpaj8hiuc5p6.apps.googleusercontent.com' #the client_id which you get from google api console
CLIENT_SECRET='gmNJI8gsjpY_AdbfEkwxajRd'					            			#the client_id which you get from google api console
AUTHORIZE_URL='https://accounts.google.com/o/oauth2/auth?'                        #get request to this url gives back the authorization code
CALLBACK_URL='http://127.0.0.1:5000/oauth2callback'								#this is the url of your website.The user is redirected to this url after the user has authorize your app.											 
ACCESS_TOKEN_URL='https://www.googleapis.com/oauth2/v3/token'				#get or post request to this url gives back the access token
API_RESOURCE_URL='https://www.googleapis.com/oauth2/v1/userinfo'          #get request to this url gives back the desired user info.
SCOPE_URL='https://www.googleapis.com/auth/user.emails.read'    #since we need users profile information 